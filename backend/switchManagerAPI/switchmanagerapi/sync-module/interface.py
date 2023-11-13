from typing import List
from ..models import Customer
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from ..db import DBCustomer, get_context_db_session
from abc import abstractmethod


class ISyncModule:
    def __init__(self):
        pass

    def compare(self, local: Customer, source: Customer) -> bool:
        """compare local / source customer"""
        if (local == source):
            return False
        return True

    @abstractmethod
    async def fetchFromSource(self) -> List[Customer]:
        """fetch customers from source"""
        pass

    async def fetchFromLocal(self, session) -> List[Customer]:
        """fetch customers from local db"""
        res: List[Customer] = []
        scalars = await session.scalars(select(DBCustomer)).all()
        for e in scalars:
            res.append(Customer.model_validate(**e.__dict__))
        return res

    async def update(self, model: Customer, session):
        """update local db"""
        await session.execute(
            insert(DBCustomer)
            .values(model.model_dump(exclude_unset=True))
            .on_conflict_do_update(
                index_elements=[DBCustomer.id],
                set_=model.model_dump(exclude_unset=True, exclude={"id"})
            )
        )

    async def sync(self):
        """sync local db with source"""
        session = await get_context_db_session()
        sources = await self.fetchFromSource()
        locals: List[Customer] = await self.fetchFromLocal()
        while (sources):
            source = sources.pop()
            local = locals.find(lambda e: e.id == source.id)
            if (local):
                # source exists in local db
                if (self.compare(local, source)):
                    # source is different from local
                    await self.update(source, session)
                locals.remove(local)
            else:
                # source does not exist in local db
                await self.update(source, session)
        # delete remaining locals (not in source)
        ids = [e.id for e in locals]
        await session.execute(
            delete(DBCustomer)
            .where(DBCustomer.id.in_(ids))
        )
