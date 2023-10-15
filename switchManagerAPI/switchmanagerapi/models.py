from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class IConnectionBase(BaseModel):
    """Base Connection model interface"""
    id: int
    name: str = Field(alias="ppp")
    port: int = 0
    toggled: bool = False
    toggleDate: Optional[datetime] = None
    type: str = "copper|fiber"

class IConnection(IConnectionBase):
    """Connection model interface"""
    """auto computed fields based on switch connection status"""
    isUp: bool = False
    proto: str = "snmp"
    speed: int = 0

class Connection(IConnection):
    """Connection Database model"""
    # relationships
    switchId: int = 0
    customerId: int = 0

class Switch(BaseModel):
    "Switch Database model"
    id: int
    name: str
    # todo create custom IP regex verification
    ip: str = "0.0.0.0"
    gpsLat: Optional[float] = None
    gpsLong: Optional[float] = None

class Customer(BaseModel):
    """Customer Database model"""
    id: int
    firstname: str
    lastname: str
    type: str
    address: str