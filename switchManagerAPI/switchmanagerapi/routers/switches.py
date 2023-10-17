from fastapi import APIRouter
from typing import Optional, Union
from ..models.factories import BatchedDeleteOutput
from ..models.switch import Switch, BatchedSwitchOutput, UpsertSwitchInput

router = APIRouter(
    tags=["v1", "switches"],
    prefix="/api/v1/switches",
    responses={404: {"description": "Not found"}},
)

# switches CRUD
@router.get("/", response_model=list[Switch])
async def listSwitches(search: Optional[str] = None):
    """return a list of switches"""
    return []

@router.get("/{id}", response_model=Switch)
async def getSwitch(id: int):
    """return a switch"""
    return Switch()

@router.post("/upsert", response_model=BatchedSwitchOutput)
async def upsertSwitch(input: Union[UpsertSwitchInput, list[UpsertSwitchInput]]):
    """upsert or udpate one || multiple switch(s)"""
    if not isinstance(input, list):
        input = [input]
    return BatchedSwitchOutput(items=[Switch()], errors=[])

@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteSwitch(ids: list[str]):
    """delete a switch"""
    return BatchedDeleteOutput(items=ids, errors=[])