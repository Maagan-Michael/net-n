from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator
from .customer import Customer
from .switch import Switch
from .factories import OrderBy, batcheableOutputFactory

## common
class IConnectionBase(BaseModel):
    """Base Connection model interface"""
    id: str = Field(min_length=3, max_length=255, description="connection id")
    name: str = Field(alias="ppp", min_length=3, max_length=255, description="connection name")
    port: int = Field(default=0, min=0, max=65535, description="port number on the switch")
    toggled: bool = Field(default=False, description="define if the port is opened")
    toggleDate: Optional[datetime] = Field(default=None, description="date at which the port should open / close based on currrent port status")
    type: str = Field(default="copper|fiber", description="physical connection type")

    @validator("toggleDate")
    def validate_toggleDate(cls, v):
        if v is not None:
            assert v > datetime.now(), "toggleDate must be in the future"
        return v

class IConnection(IConnectionBase):
    """Connection model interface"""
    """auto computed fields based on switch connection status"""
    isUp: bool = False
    proto: str = "snmp"
    speed: int = 0


## Database
class Connection(IConnection):
    """Connection Database model"""
    # relationships
    switchId: int = 0
    customerId: int = 0

## API
# connections list
class ConnectionOutput(IConnection):
    """Connection model API output"""
    # relationships
    switch: Switch = None
    customer: Customer = None

BatchConnectionOutput = batcheableOutputFactory(ConnectionOutput)

class ConnectionsOutput(BaseModel):
    """connections paginated output"""
    connections: list[ConnectionOutput] = []
    hasPrevious: bool = False
    hasNext: bool = False

class ListFilterEnum(str, Enum):
    """to filter down connections search results"""
    all = "all"
    customer = "customer"
    address = "address"
    enabled = "enabled"
    disabled = "disabled"
    up = "up"
    down = "down"
    port = "port"
    switch = "switch"

class ListSortEnum(str, Enum):
    con = "con"
    fullname = "name"
    customerId = "cid"
    address = "address"
    switch = "switch"

class ConnectionListInput(BaseModel):
    """connections list API input"""
    page: int = 0
    limit: int = Field(default=10, ge=1, le=100)
    search: Optional[str] = None
    sort: ListSortEnum = ListSortEnum.con
    order: OrderBy = OrderBy.asc
    filter: ListFilterEnum = ListFilterEnum.all

# connection update
class UpdateConnectionInput(IConnectionBase):
    """Connection model update API input"""
    pass

# connection upsert
class ConnectionUpsertInput(BaseModel):
    """Connection model upsert API input"""
    id: Optional[str] = None
    name: Optional[str] = None
    port: Optional[int] = None
    toggled: Optional[bool] = None
    toggleDate: Optional[datetime] = None
    type: Optional[str] = None
    isUp: Optional[bool] = None
    proto: Optional[str] = None
    speed: Optional[int] = None
    switchId: Optional[int] = None
    customerId: Optional[int] = None