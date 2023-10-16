from fastapi import APIRouter, Depends
from typing import Union
from ..models.connection import BatchConnectionOutput, ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput, UpdateConnectionInput

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD
@router.get("/", response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends()):
    """return a paginated list of connections"""
    return ConnectionsOutput()

@router.get("/{id}", response_model=ConnectionOutput)
async def getConnection(id: int):
    """return a connection"""
    return ConnectionOutput()

@router.post("/upsert", response_model=BatchConnectionOutput)
async def upsertConnection(input: Union[ConnectionUpsertInput, list[ConnectionUpsertInput]]):
    """upsert or udpate one || multiple connections"""
    BatchConnectionOutput(items=[ConnectionOutput()], errors=[])

@router.delete("/delete/{id}", response_model=str)
async def deleteConnection(id: int):
    """delete a connection"""
    return id