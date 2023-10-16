from fastapi import APIRouter
from switchmanagerapi.models import Customer
from typing import Union

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

@router.post("/upsert", response_model=Union[Customer, list[Customer]])
async def createCustomer(input: Union[Customer, list[Customer]]):
    """create a customer"""
    if (isinstance(input, list)):
        return [Customer()]
    return Customer()

@router.post("/update/{id}", response_model=Customer)
async def updateCustomer(input: Customer):
    """update a customer"""
    return Customer()

@router.delete("/delete/{id}", response_model=str)
async def deleteCustomer(id: int):
    """delete a customer"""
    return id