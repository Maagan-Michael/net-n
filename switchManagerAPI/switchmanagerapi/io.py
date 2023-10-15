from enum import Enum, IntEnum
from pydantic import BaseModel, Field
from .models import IConnectionBase, IConnection, Switch, Customer
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

class ListFilterEnum(IntEnum):
    """to filter down connections search results"""
    all = 0
    customer = 1
    address = 2
    toggled = 3
    notToggled = 4
    up = 5
    down = 6
    port = 7
    switch = 8

class ConnectionListInput(BaseModel):
    """connections list API input"""
    page: int = 0
    limit: int = 10
    sort: str = "id"
    search: Optional[str] = None
    order: OrderEnum = OrderEnum.asc
    filter: ListFilterEnum = ListFilterEnum.all

# connection update
class ConnectionInput(IConnectionBase):
    """Connection model update API input"""
    pass