from sqlalchemy.orm import Session
from . import Base


def upsert(db: Session, model: Base):
    """upsert a model"""
    db.merge(model)
    db.commit()
    db.refresh(model)


def batchDelete(db: Session, model: Base, ids: list[str]):
    """delete a model"""
    db.delete(model).where(model.id.in_(ids))
    db.commit()
    return ids
