from fastapi import APIRouter
from typing import Optional, Union
from ..models import BatchedDeleteOutput, Customer, BatchedCustomerOutput, UpsertCustomerInput
from ..db.factories import CustomerRepository

router = APIRouter(
    tags=["v1", "customers"],
    prefix="/api/v1/customers",
    responses={404: {"description": "Not found"}},
)

# customers CRUD


@router.get("/", response_model=list[Customer])
async def listCustomers(search: Optional[str], repo: CustomerRepository):
    return repo.list(search)


@router.get("/{id}", response_model=Customer)
async def getCustomer(id: str, repo: CustomerRepository):
    """return a customer"""
    return repo.get(id)


@router.post("/upsert", response_model=BatchedCustomerOutput)
async def upsertCustomer(input: Union[UpsertCustomerInput, list[UpsertCustomerInput]], repo: CustomerRepository):
    """upsert or udpate one || multiple customer(s)"""
    [items, errors, previousValues] = await repo.batch_upsert(input)
    return BatchedCustomerOutput.model_construct(items=items, errors=errors)


@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteCustomer(ids: list[str], repo: CustomerRepository):
    """delete a customer"""
    return repo.delete(ids)
