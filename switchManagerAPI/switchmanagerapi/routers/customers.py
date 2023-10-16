from fastapi import APIRouter
from switchmanagerapi.models import Customer

router = APIRouter(
    tags=["v1"],
    prefix="/api/v1",
    responses={404: {"description": "Not found"}},
)

# customers CRUD
@router.get("/customers", tags=["v1"], response_model=list[Customer])
async def listCustomers() -> list[Customer]:
    """return a list of customers"""
    return []

@router.get("/customer/{id}", tags=["v1"], response_model=Customer)
async def getCustomer(id: int) -> Customer:
    """return a customer"""
    return Customer()

@router.post("/customer/create", tags=["v1"], response_model=Customer)
async def createCustomer(input: Customer) -> Customer:
    """create a customer"""
    return Customer()

@router.post("/customer/update/{id}", tags=["v1"], response_model=Customer)
async def updateCustomer(input: Customer) -> Customer:
    """update a customer"""
    return Customer()

@router.delete("/customer/delete/{id}", tags=["v1"], response_model=str)
async def deleteCustomer(id: int) -> str:
    """delete a customer"""
    return id