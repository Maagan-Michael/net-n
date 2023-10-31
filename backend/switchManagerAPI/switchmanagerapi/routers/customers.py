from fastapi import APIRouter
from typing import Optional, Union
from ..models.factories import BatchedDeleteOutput
from ..models.customer import Customer, BatchedCustomerOutput, UpsertCustomerInput

router = APIRouter(
    tags=["v1", "customers"],
    prefix="/api/v1/customers",
    responses={404: {"description": "Not found"}},
)

# customers CRUD
@router.get("/", response_model=list[Customer])
async def listCustomers(search: Optional[str] = None):
    """return a list of customers"""
    return []

@router.get("/{id}", response_model=Customer)
async def getCustomer(id: str):
    """return a customer"""
    return Customer()

@router.post("/upsert", response_model=BatchedCustomerOutput)
async def upsertCustomer(input: Union[UpsertCustomerInput, list[UpsertCustomerInput]]):
    """upsert or udpate one || multiple customer(s)"""
    if not isinstance(input, list):
        input = [input]
    return BatchedCustomerOutput(items=[Customer()], errors=[])

@router.post("/delete", response_model=BatchedDeleteOutput)
async def deleteCustomer(ids: list[str]):
    """delete a customer"""
    return BatchedDeleteOutput(items=ids, errors=[])