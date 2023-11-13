from typing import List
from .interface import ISyncModule
from ..models import Customer
from sqlalchemy import select
from ..db import get_context_mapped_db_session, AutoMapBase


class SQLSyncModule(ISyncModule):
    def __init__(self, url: str, table: str, map: dict):
        super().__init__(map)
        self.url = url
        self.external_table = table

    async def fetchFromSource(self):
        session = await get_context_mapped_db_session(self.url)
        table = AutoMapBase.classes[self.external_table]
        scalars = await session.scalars(select(table)).all()
        res: List[Customer] = []
        for e in scalars:
            res.append(self.mapSourceToLocal(e.__dict__))
        return res
