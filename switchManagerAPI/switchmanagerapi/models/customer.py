from typing import Optional
from pydantic import BaseModel, Field
from .factories import batcheableOutputFactory

# Database

class Customer(BaseModel):
    """Customer Database model"""
    id: str = Field(min_length=3, max_length=255, description="customer id / worker id")
    firstname: str = Field(min_length=1, max_length=255)
    lastname: str = Field(min_length=1, max_length=255)
    type: str = Field(min_length=1, max_length=255, description="customer type (company name || person status)")
    address: str = Field(min_length=1, max_length=255)

# API
#outputs
BatchedCustomerOutput = batcheableOutputFactory(Customer)

#inputs
class UpsertCustomerInput(BaseModel):
    id: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None