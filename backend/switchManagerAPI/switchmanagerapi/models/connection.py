from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, validator, computed_field, UUID4
from .customer import Customer
from .switch import Switch
from .factories import OrderBy, batcheableOutputFactory

# common


class IConnectionBase(BaseModel):
    """Base Connection model interface"""
    id: UUID4 = Field(min_length=3, max_length=255,
                      description="connection id")
    name: str = Field(min_length=3, max_length=255,
                      description="connection name")
    port: int = Field(default=0, min=0, max=65535,
                      description="port number on the switch")
    toggled: bool = Field(
        default=False, description="define if the port is opened")
    toggleDate: Optional[datetime] = Field(
        default=None, description="date at which the port should open / close based on currrent port status")
    type: str = Field(default="copper|fiber",
                      description="physical connection type")
    autoUpdate: bool = Field(default=True,
                             description="define if the connection should be updated automatically")
    address: str = Field(min_length=1, max_length=255)

    @validator("toggleDate")
    def validate_toggleDate(cls, v):
        if v is not None:
            assert v > datetime.now(), "toggleDate must be in the future"
        return v


class IConnection(IConnectionBase):
    """Connection model interface"""
    """auto computed fields based on switch connection status"""
    isUp: bool = False
    adapter: str = "snmp"
    speed: Optional[int] = 0


# Database
class Connection(IConnection):
    """Connection Database model"""
    model_config = ConfigDict(from_attributes=True)
    # relationships

    @computed_field(return_type=str)
    @property
    def strPort(self):
        return f"{self.port}"
    switchId: UUID4
    customerId: int

# API
# outputs

# single


class ConnectionOutput(IConnection):
    model_config = ConfigDict(from_attributes=True)
    """Connection model API output"""
    # relationships
    switch: Switch
    customer: Customer


# upsert
BatchConnectionOutput = batcheableOutputFactory(ConnectionOutput)

# list


class ConnectionsOutput(BaseModel):
    """connections paginated output"""
    connections: list[ConnectionOutput] = []
    hasPrevious: bool = False
    hasNext: bool = False

# inputs
# list query input


class ListFilterEnum(str, Enum):
    """to filter down connections search results"""
    all = "all",
    customer = "customer",
    customerId = "customerId",
    address = "address",
    enabled = "enabled",
    disabled = "disabled",
    up = "up",
    down = "down",
    port = "port",
    switch = "switch",


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

# upsert


class ConnectionUpsertInput(BaseModel):
    """Connection model upsert API input"""
    id: Optional[str] = None
    name: Optional[str] = None
    port: Optional[int] = None
    toggled: Optional[bool] = None
    toggleDate: Optional[datetime] = None
    type: Optional[str] = None
    isUp: Optional[bool] = None
    adapter: Optional[str] = None
    speed: Optional[int] = None
    switchId: Optional[UUID4] = None
    customerId: Optional[int] = None
    autoUpdate: Optional[bool] = None
    address: Optional[str] = None
