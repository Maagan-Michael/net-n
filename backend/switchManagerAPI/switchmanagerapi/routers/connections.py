from fastapi import APIRouter, Depends
from typing import List, Optional, Union
from ..adapters.sync import AppAdapter
from sqlalchemy import Column, or_, select, and_
from sqlalchemy.orm import contains_eager
from ..models import BatchedDeleteOutput, OrderBy, Connection, \
    BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput, ListFilterEnum, ListSortEnum
from ..db import DBConnection, DBSwitch, DBCustomer, ConnectionRepository
import re
from ..logger import get_logger

logger = get_logger("ConnectionRouter")

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
    ListSortEnum.address: [DBConnection.address],
    ListSortEnum.fullname: [DBCustomer.lastname, DBCustomer.firstname],
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
        isMultiWord = wc > 1
        orSearch = "(^|{\s}?)" + \
            f"({'|'.join(search)}).*" if wc > 1 else f".*{search[0]}.*"
        print(orSearch)
        andSearch = f".*{'.*'.join(search)}.*"
        if (filter == ListFilterEnum.customerId):
            filters.append(DBCustomer.idstr.op('~*')(orSearch))
        elif (filter == ListFilterEnum.address):
            filters.append(DBConnection.address.op('~*')(andSearch))
        elif (filter == ListFilterEnum.port):
            filters.append(DBConnection.strPort.op('~*')(orSearch))
        elif (filter == ListFilterEnum.switch):
            filters.append(DBSwitch.name.op('~*')(orSearch))
        else:
            if (filter == ListFilterEnum.customer):
                operator = and_ if isMultiWord else or_
                filters.append(
                    operator(
                        DBCustomer.firstname.op('~*')(orSearch),
                        DBCustomer.lastname.op('~*')(orSearch),
                    )
                )
            elif (isMultiWord):
                # general search
                filters.append(
                    or_(
                        and_(
                            DBCustomer.firstname.op('~*')(orSearch),
                            DBCustomer.lastname.op('~*')(orSearch),
                        ),
                        DBConnection.address.op('~*')(andSearch),
                        and_(
                            DBSwitch.name.op('~*')(orSearch),
                            DBConnection.strPort.op('~*')(orSearch),
                        )
                    )
                )
            else:
                filters.append(or_(
                    DBConnection.name.op('~*')(orSearch),
                    DBCustomer.idstr.op('~*')(orSearch),
                    DBConnection.strPort.op('~*')(orSearch),
                    # todo handle spaces in orSearch for firstname + lastname
                    DBCustomer.firstname.op('~*')(orSearch),
                    DBCustomer.lastname.op('~*')(orSearch),
                    DBConnection.address.op('~*')(andSearch),
                    DBSwitch.name.op('~*')(orSearch),
                ))
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
        .join(DBConnection.customer, isouter=True)
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
        .join(DBConnection.customer, isouter=True)
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
    [items, errors, previousValues] = await repo.batch_upsert(input)
    ids = [e.id for e in items]
    items = (await repo.session.scalars(
        select(DBConnection)
        .join(DBConnection.customer, isouter=True)
        .join(DBConnection.switch)
        .options(contains_eager(DBConnection.customer), contains_eager(DBConnection.switch))
        .where(DBConnection.id.in_(ids))
        .execution_options(populate_existing=True)
    )).all()
    for (idx, e) in enumerate(previousValues):
        if e:
            items[idx] = ConnectionOutput.model_construct(
                **items[idx].__dict__)
            b = items[idx]
            try:
                if (e.toggled != b.toggled):
                    # enable / disable connection with adapter
                    logger.info(
                        f"toggling {'on' if b.toggled else 'off'} connection {b.id} on {b.switch.name}({b.switch.ip}:{b.port})")
                    AppAdapter.adapter.togglePort(
                        b.switch.ip, b.port, b.toggled)
                if (e.port != b.port):
                    # closing old port with adapter
                    logger.info(
                        f"port changed on connection ({b.name})({b.id}) closing old port {e.port}")
                    AppAdapter.adapter.togglePort(
                        b.switch.ip, b.port, b.toggled)
                    AppAdapter.adapter.togglePort(
                        b.switch.ip, e.port, False)
            except Exception as ex:
                logger.error(ex)
                raise Exception(
                    "asked operation on network failed, please try again")
    return BatchConnectionOutput.model_construct(items=items, errors=errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteConnection(ids: list[str], repo: ConnectionRepository):
    """delete a connection"""
    return repo.delete(ids)
