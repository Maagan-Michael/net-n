from fastapi import APIRouter
from typing import Union
from ..models.switch import Switch, BatchedSwitchOutput, UpsertSwitchInput

router = APIRouter(
    tags=["v1", "switches"],
    prefix="/api/v1/switches",
    responses={404: {"description": "Not found"}},
)

# switches CRUD
@router.get("/", response_model=list[Switch])
async def listSwitches():
    """return a list of switches"""
    return []

@router.get("/{id}", response_model=Switch)
async def getSwitch(id: int):
    """return a switch"""
    return Switch()

@router.post("/upsert", response_model=BatchedSwitchOutput)
async def upsertSwitch(input: Union[UpsertSwitchInput, list[UpsertSwitchInput]]):
    """upsert or udpate one || multiple switch(s)"""
    if (isinstance(input, list)):
        return BatchedSwitchOutput(items=[Switch()], errors=[])

@router.delete("/delete/{id}", response_model=str)
async def deleteSwitch(id: int):
    """delete a switch"""
    return id