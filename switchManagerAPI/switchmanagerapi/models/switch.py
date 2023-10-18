from typing import Optional
from pydantic import BaseModel, Field, validator
import re
from .factories import batcheableOutputFactory

IP_REGXP = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')

# Database
class Switch(BaseModel):
    "Switch Database model"
    id: str = Field(min_length=3, max_length=255, description="switch unique name / id") # switch name
    ip: str = Field(default="0.0.0.0", min_length=7, max_length=15, description="switch ip address")
    gpsLat: Optional[float] = Field(default=None, min=-90, max=90)
    gpsLong: Optional[float] = Field(default=None, min=-180, max=180)
    name: str
    description: str

    @validator("ip")
    def validate_ip(cls, v):
        assert IP_REGXP.match(v) is not None, "ip must be a valid IPv4/IPv6 address"
        return v

# API
#outputs
BatchedSwitchOutput = batcheableOutputFactory(Switch)

#inputs
class UpsertSwitchInput(BaseModel):
    id: Optional[str] = None
    ip: Optional[str] = None
    gpsLat: Optional[float] = None
    gpsLong: Optional[float] = None
    name: Optional[str] = None
    description: Optional[str] = None