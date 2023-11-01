from pydantic import BaseModel
from typing import Callable, Generic, TypeVar, List, Annotated, Union
from fastapi import Depends
from ..models.factories import BatchError
from sqlalchemy.orm import Session
from . import Base, get_db_session

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

    def __init__(self, session: Session, model: Model, validator: PydanticModel) -> None:
        self.session = session
        self.model = model
        self.validator = validator

    def get(self, id: str) -> Model:
        """return a model"""
        return self.session.select(self.model).where(self.model.id == id).first()

    def list(self, search: str = None) -> list[Model]:
        """return a list of models"""
        if search and search != "":
            return self.session.select(self.model).filter(self.model.name.like(search)).all()
        return self.session.select(self.model).all()

    def upsert(self, model: Model) -> Model:
        self.session.merge(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def batch_upsert(self, inputs: Union[Model, List[Model]]) -> (List[Model], List[BatchError]):
        """upsert multiple model(s)"""
        if not isinstance(inputs, list):
            inputs = [inputs]
        items = []
        errors = []
        for input in inputs:
            existing = None
            if input.id:
                existing = self.session.select(Model).filter(
                    Model.id == input.id).first()
            if existing:
                existing = self.validator(
                    **existing,
                    **input
                )
            else:
                existing = self.validator(**input)
            try:
                existing.model_validate()
                # upsert(db, existing)
                items.append(existing)
            except Exception as e:
                errors.append(BatchError(id=input.id, error=e))
        return (items, errors)

    def delete(self, ids: List[str]) -> List[str]:
        """batch delete model(s)"""
        self.session.delete(self.model).where(self.model.id.in_(ids))
        self.session.commit()
        return ids


def get_repository(
    model: type[Base],
    validator: type[BaseModel],
) -> Callable[[Session], DatabaseRepository]:
    def func(session: Session = Depends(get_db_session)):
        return DatabaseRepository(model, validator, session)

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
