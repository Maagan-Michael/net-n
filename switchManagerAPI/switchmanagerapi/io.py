from enum import Enum
from pydantic import BaseModel, Field
from .models import IConnectionBase, IConnection, Connection, Switch, Customer
from typing import Optional

# generic
class OrderEnum(str, Enum):
    """to order results in a paginated request"""
    asc = "asc"
    desc = "desc"

# connections list
class ConnectionOutput(IConnection):
    """Connection model API output"""
    # relationships
    switch: Switch = None
    customer: Customer = None

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
    order: OrderEnum = OrderEnum.asc
    filter: ListFilterEnum = ListFilterEnum.all

# connection update
class UpdateConnectionInput(IConnectionBase):
    """Connection model update API input"""
    pass

# connection upsert

class ConnectionUpsertInput(Connection):
    """Connection model upsert API input"""
    isUp: Optional[bool] = None
    proto: Optional[str] = None
    speed: Optional[int] = None
    switchId: Optional[int] = None
    customerId: Optional[int] = None