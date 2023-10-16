from fastapi import APIRouter
from switchmanagerapi.models import Switch

router = APIRouter(
    tags=["v1"],
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)

# switches CRUD
@router.get("/switches", tags=["v1"], response_model=list[Switch])
async def listSwitches() -> list[Switch]:
    """return a list of switches"""
    return []

@router.get("/switch/{id}", tags=["v1"], response_model=Switch)
async def getSwitch(id: int) -> Switch:
    """return a switch"""
    return Switch()

@router.post("/switch/create", tags=["v1"], response_model=Switch)
async def createSwitch(input: Switch) -> Switch:
    """create a switch"""
    return Switch()

@router.post("/switch/update/{id}", tags=["v1"], response_model=Switch)
async def updateSwitch(input: Switch) -> Switch:
    """update a switch"""
    return Switch()

@router.delete("/switch/delete/{id}", tags=["v1"], response_model=str)
async def deleteSwitch(id: int) -> str:
    """delete a switch"""
    return id