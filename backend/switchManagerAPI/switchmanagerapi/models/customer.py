from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field
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


class InternalCustomer(Customer):
    """Internal Customer Database model (used for input validation, so that the idstr is generated)"""
    @computed_field(return_type=str)
    @property
    def idstr(self):
        return f"{self.id}"


# API
# outputs
BatchedCustomerOutput = batcheableOutputFactory(Customer)

# inputs


class UpsertCustomerInput(BaseModel):
    """Customer input model"""
    id: Optional[int] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    type: Optional[str] = None
