from fastapi import APIRouter, Depends
from typing import Union
from sqlalchemy import or_, desc, asc, all_
from ..models.factories import BatchedDeleteOutput
from ..models.connection import BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput, ListSortEnum
from ..db.schemas.connections import DBConnection
from ..db.schemas.switches import DBSwitch
from ..db.schemas.customers import DBCustomer
from ..db import get_db_session
from ..db.factories import ConnectionRepository

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD
# from ..tests.mockups import createMockConnection
# createMockConnection() for i in range(10)

sortEnumMap = {
    ListSortEnum.con: [DBConnection.id],
    ListSortEnum.customerId: [DBConnection.customerId],
    ListSortEnum.fullname: [DBCustomer.lastname, DBCustomer.firstname],
    ListSortEnum.address: [DBCustomer.address],
    ListSortEnum.switch: [DBSwitch.name],
}


@router.get("/", response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends(), db=Depends(get_db_session)):
    """return a paginated list of connections"""

    connections = db.select(DBConnection).join(DBSwitch).join(DBCustomer).limit(
        input.limit).offset(input.page * input.limit)
    if (input.search.length > 0):
        if (input.filter):
            # filtered search
            connections = connections.filter(
                DBConnection[input.filter].like(input.search)
            )
        else:
            # general search
            connections = connections.filter(
                or_(
                    DBConnection.name.like(input.search),
                    DBConnection.port.like(input.search),
                    DBConnection.customerId.customerId.like(input.search),
                    # todo handle spaces in search for firstname + lastname
                    DBConnection.customer.firstname.like(input.search),
                    DBConnection.customer.lastname.like(input.search),
                    DBConnection.customer.address.like(input.search),
                    DBConnection.switch.name.like(input.search),
                )
            )
    connections = connections.sort(
        **DBConnection[sortEnumMap[input.sortBy]]
    ).all()
    return ConnectionsOutput(
        connections,
        hasPrevious=False,
        hasNext=True,
    )


@router.get("/{id}", response_model=ConnectionOutput)
async def getConnection(id: str, db=Depends(get_db_session)):
    return db.select(DBConnection).where(DBConnection.id == id).join(DBSwitch, DBCustomer).first()


@router.post("/upsert", response_model=BatchConnectionOutput)
async def upsertConnection(input: Union[ConnectionUpsertInput, list[ConnectionUpsertInput]], repo: ConnectionRepository):
    """upsert or udpate one || multiple connections"""
    [items, errors] = repo.batch_upsert(input)
    return BatchConnectionOutput(items, errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteConnection(ids: list[str], repo: ConnectionRepository):
    """delete a connection"""
    errors = []
    items = repo.delete(ids)
    # todo check for errors ?
    return BatchedDeleteOutput(items, errors)
