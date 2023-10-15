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

class ConnectionListInput(BaseModel):
    """connections list API input"""
    page: int = 0
    limit: int = 10
    sort: str = "id"
    search: Optional[str] = None
    order: OrderEnum = OrderEnum.asc
    filter: ListFilterEnum = ListFilterEnum.all

# connection update
class UpdateConnectionInput(IConnectionBase):
    """Connection model update API input"""
    pass

# connection create
class ConnectionInput(Connection):
    """Connection model create API input"""
    # relationships
    switchId: int = 0
    customerId: int = 0