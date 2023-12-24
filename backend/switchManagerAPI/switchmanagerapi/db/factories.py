import re
import sys
from pydantic import BaseModel
from typing import Callable, Generic, Optional, TypeVar, List, Annotated, Union
from fastapi import Depends, HTTPException, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from . import Base, get_db_session
from ..logger import get_logger

from ..models import BatchError, BatchedDeleteOutput, Connection, Switch, Customer
from .schemas import DBConnection, DBSwitch, DBCustomer

Model = TypeVar("Model", bound=Base)
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class DatabaseRepository(Generic[Model]):
    """common repository for crud operations on models"""

    def __init__(self, session: AsyncSession, schema: Model, model: PydanticModel, name: str) -> None:
        self.session = session
        self.schema = schema
        self.model = model
        self.logger = get_logger(name)

    async def get(self, id: str) -> Model:
        """return a model"""
        res = await self.session.scalar(select(self.schema).where(self.schema.id == id).limit(1))
        if (res is None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                details=f"not found"
            )
        return Model(res[0])

    async def list(self, search=[], limit: Optional[int] = 10) -> list[Model]:
        """return a list of models"""
        q = None
        if search and len(search) > 0:
            q = await self.session.scalars(
                select(self.schema).filter(
                    or_(*search)
                )
                .limit(limit)
            )
        else:
            q = await self.session.scalars(
                select(self.schema).limit(limit)
            )
        return [self.model.model_construct(**e.__dict__) for e in q]

    async def upsert(self, model: Model) -> Model:
        await self.session.execute(
            insert(self.schema)
            .values(model.model_dump(exclude_unset=True))
            .on_conflict_do_update(index_elements=[self.schema.id], set_=model.model_dump(exclude_unset=True, exclude={"id"}))
        )
        self.logger.info(f"upserted:{model.id}")
        return model

    async def batch_upsert(self, inputs: Union[Model, List[Model]]) -> (List[Model], List[BatchError], List[Model]):
        """upsert multiple model(s)"""
        if not isinstance(inputs, list):
            inputs = [inputs]
        items = []
        errors = []
        previousValues = []
        for input in inputs:
            existing = None
            if input.id:
                existing = await self.session.scalar(
                    select(self.schema)
                    .filter(self.schema.id == input.id)
                    .limit(1)
                )
            if existing:
                previousValues.append(
                    self.model.model_construct(**existing.__dict__))
                existing = {
                    **existing.__dict__,
                    **input.model_dump(exclude_unset=True)
                }
            else:
                previousValues.append(None)
                existing = input
            try:
                existing = self.model.model_validate(existing)
                await self.upsert(existing)
                items.append(existing)
            except Exception as e:
                if isinstance(e, SQLAlchemyError):
                    self.logger.error(e)
                errors.append(BatchError.model_construct(
                    id=input.id, error=str(e)))
                previousValues.pop()
        return (items, errors, previousValues)

    async def delete(self, ids: List[str]) -> BatchedDeleteOutput:
        """batch delete model(s)"""
        await self.session.execute(
            delete(self.schema)
            .where(self.schema.id.in_(ids))
        )
        for id in ids:
            self.logger.info(f"deleted:{id}")
        return BatchedDeleteOutput.model_construct(items=ids, errors=[])


def get_repository(
    schema: type[Base],
    model: type[BaseModel],
    name: str
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(schema=schema, model=model, session=session, name=name)
    return func


ConnectionRepository = Annotated[
    DatabaseRepository[DBConnection],
    Depends(get_repository(DBConnection, Connection, "connections"))
]

SwitchRepository = Annotated[
    DatabaseRepository[DBSwitch],
    Depends(get_repository(DBSwitch, Switch, "switches"))
]

CustomerRepository = Annotated[
    DatabaseRepository[DBCustomer],
    Depends(get_repository(DBCustomer, Customer, "customers"))
]
