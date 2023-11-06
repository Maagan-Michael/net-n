from fastapi import APIRouter, Depends
from typing import List, Union
from sqlalchemy import Column, or_, select
from ..models.factories import BatchedDeleteOutput, OrderBy
from ..models.connection import BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput, ListSortEnum
from ..db.schemas.connections import DBConnection
from ..db.schemas.switches import DBSwitch
from ..db.schemas.customers import DBCustomer
from ..db.factories import ConnectionRepository

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD
# from ..tests.mockups import createMockConnection
# createMockConnection() for i in range(10)

sortEnumMap: dict[ListSortEnum, List[Column[any]]] = {
    ListSortEnum.con: [DBConnection.id],
    ListSortEnum.customerId: [DBConnection.customerId],
    ListSortEnum.fullname: [DBCustomer.lastname, DBCustomer.firstname],
    ListSortEnum.address: [DBCustomer.address],
    ListSortEnum.switch: [DBSwitch.name],
}


@router.get("/", response_model=ConnectionsOutput)
async def listConnections(repo: ConnectionRepository, input: ConnectionListInput = Depends()):
    """return a paginated list of connections"""
    filters = []
    if (input.search and len(input.search) > 0):
        if (input.filter):
            # filtered search
            filters = [DBConnection[input.filter].like(input.search)]
        else:
            # general search
            filters = [
                or_(
                    DBConnection.name.like(input.search),
                    DBConnection.port.like(input.search),
                    DBConnection.customerId.like(input.search),
                    # todo handle spaces in search for firstname + lastname
                    DBConnection.customer.firstname.like(input.search),
                    DBConnection.customer.lastname.like(input.search),
                    DBConnection.customer.address.like(input.search),
                    DBConnection.switch.name.like(input.search),
                )
            ]
    obFields = sortEnumMap[input.sort]
    orderBy = [e.desc() for e in obFields] if input.order == OrderBy.desc else [
        e.asc() for e in obFields]
    stm = (select(DBConnection)
           .join(DBConnection.customer)
           .join(DBConnection.switch)
           .filter(*filters)
           .order_by(*orderBy)
           .limit(input.limit + 1)
           .offset(input.page * input.limit))
    print(stm)
    q = await repo.session.scalars(stm)
    # todo : compute hasPrevious
    res = [ConnectionOutput.model_construct(e) for e in q]
    print(res)
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
    q = repo.session.scalar(
        select(DBConnection)
        .where(DBConnection.id == id)
        .join(DBConnection.customer)
        .join(DBConnection.switch)
        .limit(1)
    )
    if q is not None:
        return ConnectionOutput(q)
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
