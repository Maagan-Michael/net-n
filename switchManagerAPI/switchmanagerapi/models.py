from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional
from .helpers import IP_REGXP

class IConnectionBase(BaseModel):
    """Base Connection model interface"""
    id: int
    name: str = Field(alias="ppp", min_length=3, max_length=255, description="connection name")
    port: int = Field(default=0, description="port number on the switch")
    toggled: bool = Field(default=False, description="define if the port is opened")
    toggleDate: Optional[datetime] = Field(default=None, description="date at which the port should open / close based on currrent port status")
    type: str = Field(default="copper|fiber", description="physical connection type")

    @validator("port")
    def validate_port(cls, v):
        assert v >= 0, "port must be positive"
        assert v <= 65535, "port must be lower than 65535"
        return v

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

class Connection(IConnection):
    """Connection Database model"""
    # relationships
    switchId: int = 0
    customerId: int = 0

class Switch(BaseModel):
    "Switch Database model"
    id: int
    name: str = Field(min_length=1, max_length=255)
    ip: str = "0.0.0.0"
    gpsLat: Optional[float] = None
    gpsLong: Optional[float] = None

    @validator("gpsLat")
    def validate_gpsLat(cls, v):
        if v is not None:
            assert v >= -90, "gpsLat must be greater than -90"
            assert v <= 90, "gpsLat must be lower than 90"
        return v

    @validator("gpsLong")
    def validate_gpsLong(cls, v):
        if v is not None:
            assert v >= -180, "gpsLong must be greater than -180"
            assert v <= 180, "gpsLong must be lower than 180"
        return v

    @validator("ip")
    def validate_ip(cls, v):
        assert IP_REGXP.match(v) is not None, "ip must be a valid IPv4/IPv6 address"
        return v

class Customer(BaseModel):
    """Customer Database model"""
    id: int
    firstname: str = Field(min_length=1, max_length=255)
    lastname: str = Field(min_length=1, max_length=255)
    type: str = Field(min_length=1, max_length=255, description="customer type (company name || person status)")
    address: str = Field(min_length=1, max_length=255)