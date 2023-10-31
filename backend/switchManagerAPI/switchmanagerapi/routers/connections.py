from fastapi import APIRouter, Depends
from typing import Union
from ..models.factories import BatchedDeleteOutput
from ..models.connection import BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput
from ..tests.mockups import createMockConnection
from ..db.schemas.connections import DBConnection
from ..db.schemas.switches import DBSwitch
from ..db.schemas.customers import DBCustomer
from ..db import get_db

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD

# createMockConnection() for i in range(10)


@router.get("/", response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends(), db=Depends(get_db)):
    """return a paginated list of connections"""

    connections = db.select(DBConnection)
    if (input.search.length > 0):
        # if (input.filter):
        connections = connections.filter(DBConnection.name.like(input.search))
    connections = connections.join(DBSwitch).join(DBCustomer).limit(
        input.limit).offset(input.page * input.limit).all()
    return ConnectionsOutput(
        connections,
        hasPrevious=False,
        hasNext=True,
    )


@router.get("/{id}", response_model=ConnectionOutput)
async def getConnection(id: str):
    """return a connection"""
    return createMockConnection()


@router.post("/upsert", response_model=BatchConnectionOutput)
async def upsertConnection(input: Union[ConnectionUpsertInput, list[ConnectionUpsertInput]]):
    """upsert or udpate one || multiple connections"""
    if not isinstance(input, list):
        input = [input]
    BatchConnectionOutput(items=[ConnectionOutput()], errors=[])


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteConnection(ids: list[str]):
    """delete a connection"""
    return BatchedDeleteOutput(items=ids, errors=[])
