from fastapi import APIRouter, Depends
from typing import Optional, Union
from ..models.factories import BatchError, BatchedDeleteOutput
from ..models.customer import Customer, BatchedCustomerOutput, UpsertCustomerInput
from ..db import get_db
from ..db.schemas.customers import DBCustomer
from ..db.factories import upsert, batchDelete

router = APIRouter(
    tags=["v1", "customers"],
    prefix="/api/v1/customers",
    responses={404: {"description": "Not found"}},
)

# customers CRUD


@router.get("/", response_model=list[Customer])
async def listCustomers(search: Optional[str] = None, db=Depends(get_db)):
    if search and search != "":
        return db.select(DBCustomer).filter(DBCustomer.name.like(search)).all()
    return db.select(DBCustomer).all()


@router.get("/{id}", response_model=Customer)
async def getCustomer(id: str, db=Depends(get_db)):
    """return a customer"""
    return db.select(DBCustomer).filter(DBCustomer.id == id).first()


@router.post("/upsert", response_model=BatchedCustomerOutput)
async def upsertCustomer(input: Union[UpsertCustomerInput, list[UpsertCustomerInput]], db=Depends(get_db)):
    """upsert or udpate one || multiple customer(s)"""
    if not isinstance(input, list):
        input = [input]
    items = []
    errors = []
    for customer in input:
        existing = None
        if customer.id:
            existing = db.select(DBCustomer).filter(
                DBCustomer.id == customer.id).first()
        if existing:
            existing = Customer(
                **existing,
                **customer
            )
        else:
            existing = Customer(**customer)
        try:
            existing.model_validate()
            upsert(db, existing)
            items.append(existing)
        except Exception as e:
            errors.append(BatchError(id=customer.id, error=e))
    return BatchedCustomerOutput(items, errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteCustomer(ids: list[str], db=Depends(get_db)):
    """delete a customer"""
    batchDelete(db, DBCustomer, ids)
    return BatchedDeleteOutput(items=ids, errors=[])
