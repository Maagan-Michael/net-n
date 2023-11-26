from fastapi import APIRouter
from typing import Optional, Union

from sqlalchemy import update
from ..models.factories import BatchedDeleteOutput
from ..models.switch import Switch, BatchedSwitchOutput, UpsertSwitchInput
from ..db.schemas import DBConnection
from ..db.factories import SwitchRepository

router = APIRouter(
    tags=["v1", "switches"],
    prefix="/api/v1/switches",
    responses={404: {"description": "Not found"}},
)

# switches CRUD


@router.get("/", response_model=list[Switch])
async def listSwitches(search: Optional[str], repo: SwitchRepository):
    """return a list of switches"""
    return repo.list(search)


@router.get("/{id}", response_model=Switch)
async def getSwitch(id: int, repo: SwitchRepository):
    """return a switch"""
    return repo.get(id)


@router.post("/upsert", response_model=BatchedSwitchOutput)
async def upsertSwitch(input: Union[UpsertSwitchInput, list[UpsertSwitchInput]], repo: SwitchRepository):
    """upsert or udpate one || multiple switch(s)"""
    [items, errors] = await repo.batch_upsert(input)
    restricted = [e.id for e in items if e.restricted]
    print(restricted)
    if len(restricted) > 0:
        await repo.session.execute(
            update(DBConnection)
            .where(DBConnection.switchId.in_(restricted))
            .values(autoUpdate=False)
        )
    return BatchedSwitchOutput.model_construct(items=items, errors=errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteSwitch(ids: list[str], repo: SwitchRepository):
    """delete switch(es)"""
    return repo.delete(ids)
