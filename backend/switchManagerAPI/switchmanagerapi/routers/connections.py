from fastapi import APIRouter, Depends
from typing import List, Optional, Union
from sqlalchemy import Column, or_, select, and_
from sqlalchemy.orm import contains_eager
from ..models.factories import BatchedDeleteOutput, OrderBy
from ..models.customer import Customer
from ..models.switch import Switch
from ..models.connection import BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput, ListFilterEnum, ListSortEnum
from ..db.schemas.connections import DBConnection
from ..db.schemas.switches import DBSwitch
from ..db.schemas.customers import DBCustomer
from ..db.factories import ConnectionRepository
import re

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD
# from ..tests.mockups import createMockConnection
# createMockConnection() for i in range(10)

sortEnumMap: dict[ListSortEnum, List[Column[any]]] = {
    ListSortEnum.con: [DBConnection.name],
    ListSortEnum.customerId: [DBConnection.customerId],
    ListSortEnum.fullname: [DBCustomer.lastname, DBCustomer.firstname],
    ListSortEnum.address: [DBCustomer.address],
    ListSortEnum.switch: [DBSwitch.name],
}


def getFilterStm(search: Optional[str], filter: ListFilterEnum):
    filters = []
    # status filters
    if (filter == ListFilterEnum.enabled):
        filters.append(DBConnection.toggled == True)
    elif (filter == ListFilterEnum.disabled):
        filters.append(DBConnection.toggled == False)
    elif (filter == ListFilterEnum.up):
        filters.append(DBConnection.isUp == True)
    elif (filter == ListFilterEnum.down):
        filters.append(DBConnection.isUp == False)

    if (search and len(search) > 0):
        search = [re.escape(e) for e in search.strip().split(" ")]
        wc = len(search)
        orSearch = "%(" + "|".join(search) + \
            ")%" if wc > 1 else "%" + search[0] + "%"
        andSearch = "%" + "%".join(search) + "%"
        if (filter == ListFilterEnum.customerId):
            filters.append(DBConnection.customerId.like(orSearch))
        elif (filter == ListFilterEnum.address):
            filters.append(DBCustomer.address.like(andSearch))
        elif (filter == ListFilterEnum.port):
            filters.append(DBConnection.port.like(orSearch))
        elif (filter == ListFilterEnum.switch):
            filters.append(DBSwitch.name.like(orSearch))
        else:
            if (filter == ListFilterEnum.customer):
                operator = and_ if wc > 1 else or_
                filters.append(
                    operator(
                        DBCustomer.firstname.like(orSearch),
                        DBCustomer.lastname.like(orSearch),
                    )
                )
            else:
                # general search
                filters.append(
                    or_(
                        DBConnection.name.like(orSearch),
                        DBConnection.port.like(orSearch),
                        DBConnection.customerId.like(orSearch),
                        # todo handle spaces in orSearch for firstname + lastname
                        DBCustomer.firstname.like(orSearch),
                        DBCustomer.lastname.like(orSearch),
                        DBCustomer.address.like(orSearch),
                        DBSwitch.name.like(orSearch),
                    )
                )
    return filters


@router.get("/", response_model=ConnectionsOutput)
async def listConnections(repo: ConnectionRepository, input: ConnectionListInput = Depends()):
    """return a paginated list of connections"""
    filters = getFilterStm(input.search, input.filter)
    obFields = sortEnumMap[input.sort]
    orderBy = [e.desc() for e in obFields] if input.order == OrderBy.desc else [
        e.asc() for e in obFields]
    stm = (
        select(DBConnection)
        .join(DBConnection.customer)
        .join(DBConnection.switch)
        .options(contains_eager(DBConnection.customer), contains_eager(DBConnection.switch))
        .filter(*filters)
        .order_by(*orderBy)
        .limit(input.limit + 1)
        .offset(input.page * input.limit)
        .execution_options(populate_existing=True)
    )
    q = await repo.session.scalars(stm)
    # todo : compute hasPrevious
    res = []
    for e in q:
        connection = ConnectionOutput.model_construct(**e.__dict__)
        res.append(connection)
    hasPrevious = input.page > 0
    hasNext = len(res) > input.limit
    if (hasNext):
        res.pop()
    return ConnectionsOutput(
        connections=res,
        hasNext=hasNext,
        hasPrevious=hasPrevious,
    )


@router.get("/{id}", response_model=ConnectionOutput)
async def getConnection(id: str, repo: ConnectionRepository):
    q = await repo.session.scalar(
        select(DBConnection)
        .join(DBConnection.customer)
        .join(DBConnection.switch)
        .options(contains_eager(DBConnection.customer), contains_eager(DBConnection.switch))
        .where(DBConnection.id == id)
        .execution_options(populate_existing=True)
        .limit(1)
    )
    if q is not None:
        return ConnectionOutput.model_construct(**q.__dict__)
    return None


@router.post("/upsert", response_model=BatchConnectionOutput)
async def upsertConnection(input: Union[ConnectionUpsertInput, list[ConnectionUpsertInput]], repo: ConnectionRepository):
    """upsert or udpate one || multiple connections"""
    [items, errors] = repo.batch_upsert(input)
    return BatchConnectionOutput(items, errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteConnection(ids: list[str], repo: ConnectionRepository):
    """delete a connection"""
    return repo.delete(ids)
