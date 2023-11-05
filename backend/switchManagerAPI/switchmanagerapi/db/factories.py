from pydantic import BaseModel
from typing import Callable, Generic, TypeVar, List, Annotated, Union
from fastapi import Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from . import Base, get_db_session

from ..models.factories import BatchError, BatchedDeleteOutput
from .schemas.connections import DBConnection
from .schemas.switches import DBSwitch
from .schemas.customers import DBCustomer
from ..models.connection import Connection
from ..models.switch import Switch
from ..models.customer import Customer

Model = TypeVar("Model", bound=Base)
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class DatabaseRepository(Generic[Model]):
    """common repository for crud operations on models"""

    def __init__(self, session: AsyncSession, schema: Model, model: PydanticModel) -> None:
        self.session = session
        self.schema = schema
        self.model = model

    async def get(self, id: str) -> Model:
        """return a model"""
        res = await self.session.scalar(select(self.schema).where(self.schema.id == id).limit(1))
        if (res is None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                details=f"not found"
            )
        return Model(res[0])

    async def list(self, search: str = None) -> list[Model]:
        """return a list of models"""
        q = None
        if search and search != "":
            q = await self.session.scalars(
                select(self.schema).filter(self.schema.name.like(search)))
        else:
            q = await self.session.scalars(select(self.schema))
        return [Model(e) for e in q]

    async def upsert(self, model: Model) -> Model:
        await self.session.merge(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def batch_upsert(self, inputs: Union[Model, List[Model]]) -> (List[Model], List[BatchError]):
        """upsert multiple model(s)"""
        if not isinstance(inputs, list):
            inputs = [inputs]
        items = []
        errors = []
        for input in inputs:
            existing = None
            if input.id:
                existing = await self.session.scalar(select(self.schema).filter(self.schema.id == input.id))
            if existing:
                existing = self.model(
                    **existing,
                    **input
                )
            else:
                existing = self.model(**input)
            try:
                existing.model_validate()
                self.upsert(existing)
                items.append(existing)
            except Exception as e:
                errors.append(BatchError(id=input.id, error=e))
        return (items, errors)

    async def delete(self, ids: List[str]) -> BatchedDeleteOutput:
        """batch delete model(s)"""
        await self.session.execute(
            delete(self.schema)
            .where(self.schema.id.in_(ids))
        )
        return BatchedDeleteOutput(items=ids, errors=[])


def get_repository(
    schema: type[Base],
    model: type[BaseModel],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(schema=schema, model=model, session=session)

    return func


ConnectionRepository = Annotated[
    DatabaseRepository[DBConnection],
    Depends(get_repository(DBConnection, Connection))
]

SwitchRepository = Annotated[
    DatabaseRepository[DBSwitch],
    Depends(get_repository(DBSwitch, Switch))
]

CustomerRepository = Annotated[
    DatabaseRepository[DBCustomer],
    Depends(get_repository(DBCustomer, Customer))
]
