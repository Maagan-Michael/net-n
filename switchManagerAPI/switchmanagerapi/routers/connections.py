from fastapi import APIRouter, Depends
from typing import Union
from switchmanagerapi.io import ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionUpsertInput, UpdateConnectionInput

router = APIRouter(
    tags=["v1", "connections"],
    prefix="/api/v1/connections",
    responses={404: {"description": "Not found"}},
)

# connections CRUD
# connections CRUD
@router.get("/", response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends()):
    """return a paginated list of connections"""
    return ConnectionsOutput()

@router.get("/{id}", response_model=ConnectionOutput)
async def getConnection(id: int):
    """return a connection"""
    return ConnectionOutput()

@router.post("/upsert", response_model=Union[ConnectionOutput, list[ConnectionOutput]])
async def createConnection(input: Union[ConnectionUpsertInput, list[ConnectionUpsertInput]]):
    """create one / upsert multiple connections"""
    if (isinstance(input, list)):
        return [ConnectionOutput()]
    return ConnectionOutput()

@router.post("/update/{id}", response_model=ConnectionOutput)
async def updateConnection(input: UpdateConnectionInput):
    """update a connection"""
    return ConnectionOutput()

@router.delete("/delete/{id}", response_model=str)
async def deleteConnection(id: int):
    """delete a connection"""
    return id