import re
from fastapi import APIRouter
from typing import Optional, Union

from sqlalchemy import update
from ..models.factories import BatchedDeleteOutput
from ..models.switch import Switch, BatchedSwitchOutput, UpsertSwitchInput
from ..db.schemas import DBSwitch, DBConnection
from ..db.factories import SwitchRepository

router = APIRouter(
    tags=["v1", "switches"],
    prefix="/api/v1/switches",
    responses={404: {"description": "Not found"}},
)

# switches CRUD


@router.get("/", response_model=list[Switch])
async def listSwitches(search: Optional[str], limit: Optional[int], repo: SwitchRepository):
    """return a list of switches"""
    searchOperators = []
    if (search and len(search) > 0):
        search = re.escape(search)
        DBSwitch.name.op("~*")(search)

    return await repo.list(searchOperators, limit)


@router.get("/{id}", response_model=Switch)
async def getSwitch(id: int, repo: SwitchRepository):
    """return a switch"""
    return repo.get(id)


@router.post("/upsert", response_model=BatchedSwitchOutput)
async def upsertSwitch(input: Union[UpsertSwitchInput, list[UpsertSwitchInput]], repo: SwitchRepository):
    """
        upsert or udpate one || multiple switch(s)
        if a switch moved to restricted, then the autoUpdate flag is set to False
        TODO: if restrictedPorts changed, then update the connections.autoUpdate accordingly
    """
    [items, errors, previousValues] = await repo.batch_upsert(input)
    restricted = [e.id for e in items if e.restricted]
    if len(restricted) > 0:
        await repo.session.execute(
            update(DBConnection)
            .where(DBConnection.switchId.in_(restricted))
            .values(autoUpdate=False)
        )
    return BatchedSwitchOutput.model_construct(items=items, errors=errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteSwitch(ids: list[str], repo: SwitchRepository):
    """
        delete switch(es)
        TODO: close all connections to the switch(es)
        TODO: remove all associated connections
    """
    return repo.delete(ids)
