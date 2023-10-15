from enum import Enum, IntEnum
from pydantic import BaseModel
from .models import ConnectionInterface, Switch, Customer

# generic
class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"

# connections list
class ConnectionOutput(ConnectionInterface):
    # relationships
    switch: Switch = None
    customer: Customer = None

class ConnectionsOutput(BaseModel):
    connections: list[ConnectionOutput] = []
    hasPrevious: bool = False
    hasNext: bool = False

class ListFilterEnum(IntEnum):
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
    page: int = 0
    limit: int = 10
    sort: str = "id"
    search: str = ""
    order: OrderEnum = OrderEnum.asc
    filter: ListFilterEnum = ListFilterEnum.all