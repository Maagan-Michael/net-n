from fastapi import APIRouter, Depends
from typing import Optional, Union
from ..models.factories import BatchError, BatchedDeleteOutput
from ..models.switch import Switch, BatchedSwitchOutput, UpsertSwitchInput
from ..db import get_db
from ..db.schemas.switches import DBSwitch
from ..db.factories import upsert, batchDelete

router = APIRouter(
    tags=["v1", "switches"],
    prefix="/api/v1/switches",
    responses={404: {"description": "Not found"}},
)

# switches CRUD


@router.get("/", response_model=list[Switch])
async def listSwitches(search: Optional[str] = None, db=Depends(get_db)):
    """return a list of switches"""
    if search and search != "":
        return db.select(DBSwitch).filter(DBSwitch.name.like(search)).all()
    return db.select(DBSwitch).all()


@router.get("/{id}", response_model=Switch)
async def getSwitch(id: int, db=Depends(get_db)):
    """return a switch"""
    return db.select(DBSwitch).filter(DBSwitch.id == id).first()


@router.post("/upsert", response_model=BatchedSwitchOutput)
async def upsertSwitch(input: Union[UpsertSwitchInput, list[UpsertSwitchInput]], db=Depends(get_db)):
    """upsert or udpate one || multiple switch(s)"""
    items = []
    errors = []
    if not isinstance(input, list):
        input = [input]
    for switch in input:
        existing = None
        if switch.id:
            existing = db.select(DBSwitch).filter(
                DBSwitch.id == switch.id).first()
        if existing:
            existing = Switch(
                **existing,
                **switch
            )
        else:
            existing = Switch(**switch)
        try:
            existing.model_validate()
            upsert(db, existing)
            items.append(existing)
        except Exception as e:
            errors.append(BatchError(id=switch.id, error=e))
    return BatchedSwitchOutput(items=[Switch()], errors=[])


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteSwitch(ids: list[str], db=Depends(get_db)):
    """delete a switch"""
    batchDelete(db, DBSwitch, ids)
    return BatchedDeleteOutput(items=ids, errors=[])
