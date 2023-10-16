from fastapi import APIRouter, Depends
from switchmanagerapi.io import ConnectionOutput, ConnectionsOutput, ConnectionListInput, ConnectionInput, UpdateConnectionInput

router = APIRouter(
    tags=["v1"],
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)

# connections CRUD
# connections CRUD
@router.get("/connections", tags=["v1"], response_model=ConnectionsOutput)
async def listConnections(input: ConnectionListInput = Depends()) -> ConnectionsOutput:
    """return a paginated list of connections"""
    return ConnectionsOutput()

@router.get("/connection/{id}", tags=["v1"], response_model=ConnectionOutput)
async def getConnection(id: int) -> ConnectionOutput:
    """return a connection"""
    return ConnectionOutput()

@router.post("/connection/create", tags=["v1"], response_model=ConnectionOutput)
async def createConnection(input: ConnectionInput) -> ConnectionOutput:
    """create a connection"""
    return ConnectionOutput()

@router.post("/connection/update/{id}", tags=["v1"], response_model=ConnectionOutput)
async def updateConnection(input: UpdateConnectionInput) -> ConnectionOutput:
    """update a connection"""
    return ConnectionOutput()

@router.delete("/connection/delete/{id}", tags=["v1"], response_model=str)
async def deleteConnection(id: int) -> str:
    """delete a connection"""
    return id