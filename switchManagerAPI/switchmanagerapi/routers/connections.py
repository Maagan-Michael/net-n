from fastapi import APIRouter, Depends
from typing import Union
from ..models.factories import BatchedDeleteOutput
from ..models.connection import BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput
from ..tests.mockups import createMockConnection

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD


@router.get("/", response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends()):
    """return a paginated list of connections"""
    return ConnectionsOutput(
        items=[createMockConnection() for i in range(10)],
        hasPrevious=False,
        hasNext=True,
    )


@router.get("/{id}", response_model=ConnectionOutput)
async def getConnection(id: str):
    """return a connection"""
    return ConnectionOutput()


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
