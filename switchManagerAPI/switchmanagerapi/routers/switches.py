from fastapi import APIRouter
from switchmanagerapi.models import Switch
from typing import Union

router = APIRouter(
    tags=["v1", "switchs"],
    prefix="/api/v1/switchs",
    responses={404: {"description": "Not found"}},
)

# switches CRUD
@router.get("/", response_model=list[Switch])
async def listSwitches():
    """return a list of switchs"""
    return []

@router.get("/{id}", response_model=Switch)
async def getSwitch(id: int):
    """return a switch"""
    return Switch()

@router.post("/upsert", response_model=Union[Switch, list[Switch]])
async def createSwitch(input: Union[Switch, list[Switch]]):
    """upsert one / multiple switch(s)"""
    if (isinstance(input, list)):
        return [Switch()]
    return Switch()

@router.post("/update/{id}", response_model=Switch)
async def updateSwitch(input: Switch):
    """update a switch"""
    return Switch()

@router.delete("/delete/{id}", response_model=str)
async def deleteSwitch(id: int):
    """delete a switch"""
    return id