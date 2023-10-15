from datetime import datetime
from pydantic import BaseModel, Field

class ConnectionInterface(BaseModel):
    id: int
    name: str = Field(alias="ppp")
    port: int = 0
    toggled: bool = False
    isUp: bool = False
    toggleDate: datetime = None
    proto: str = "snmp"
    speed: int = 0
    type: str = "copper|fiber"

class Connection(ConnectionInterface):
    # relationships
    switchId: int = 0
    customerId: int = 0

class Switch(BaseModel):
    id: int
    name: str
    # todo create custom IP regex verification
    ip: str = "0.0.0.0"
    gpsLat: float = 0.0
    gpsLong: float = 0.0

class Customer(BaseModel):
    id: int
    firstname: str
    lastname: str
    type: str
    address: str