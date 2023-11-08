from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from .factories import batcheableOutputFactory

# Database


class Customer(BaseModel):
    """Customer Database model"""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(min=0, description="customer id / worker id")
    firstname: str = Field(min_length=1, max_length=255)
    lastname: str = Field(min_length=1, max_length=255)
    type: str = Field(min_length=1, max_length=255,
                      description="customer type (company name || person status)")
    address: str = Field(min_length=1, max_length=255)


class InternalCustomer(Customer):
    idstr: str = Field(min_length=1, max_length=255,
                       description="id string projection")


# API
# outputs
BatchedCustomerOutput = batcheableOutputFactory(Customer)

# inputs


class UpsertCustomerInput(BaseModel):
    id: Optional[int] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None
