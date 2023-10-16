from fastapi import APIRouter
from typing import Union
from ..models.customer import Customer, BatchedCustomerOutput, UpserCustomerInput

router = APIRouter(
    tags=["v1", "customers"],
    prefix="/api/v1/customers",
    responses={404: {"description": "Not found"}},
)

# customers CRUD
@router.get("/", response_model=list[Customer])
async def listCustomers():
    """return a list of customers"""
    return []

@router.get("/{id}", response_model=Customer)
async def getCustomer(id: int):
    """return a customer"""
    return Customer()

@router.post("/upsert", response_model=BatchedCustomerOutput)
async def upsertCustomer(input: Union[UpserCustomerInput, list[UpserCustomerInput]]):
    """upsert or udpate one || multiple customer(s)"""
    return BatchedCustomerOutput(items=[Customer()], errors=[])

@router.delete("/delete/{id}", response_model=str)
async def deleteCustomer(id: int):
    """delete a customer"""
    return id