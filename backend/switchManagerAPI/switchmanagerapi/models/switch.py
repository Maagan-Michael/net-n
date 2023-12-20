from typing import Optional
from pydantic import BaseModel, Field, validator, UUID4
import re
from .factories import batcheableOutputFactory

IP_REGXP = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')

# Database


class Switch(BaseModel):
    "Switch Database model"
    id: UUID4 = Field(min_length=3, max_length=255,
                      description="switch unique name / id")  # switch name
    ip: str = Field(default="0.0.0.0", min_length=7,
                    max_length=15, description="switch ip address")
    gpsLat: Optional[float] = Field(default=None, min=-90, max=90)
    gpsLong: Optional[float] = Field(default=None, min=-180, max=180)
    name: str
    description: str
    notReachable: bool = Field(
        default=False, description="the switch disapeared from the network"
    )
    restricted: bool = Field(
        default=False, description="switch access / update is restricted")
    restrictedPorts: list[int] = Field(
        default=[], description="restricted ports"
    )
    restrictedPortsDesc: list[str] = Field(
        default=[], description="restricted ports description, indexed by restrictedPorts"
    )

    @validator("restrictedPorts")
    def validate_restrictedPorts(cls, v):
        assert len(v) == len(
            set(v)), "restrictedPorts must be unique"
        return v

    @validator("restrictedPortsDesc")
    def validate_restrictedPortsDesc(cls, v, values):
        assert len(v) == len(
            values["restrictedPorts"]), "restrictedPortsDesc must have the same length as restrictedPorts"
        return v

    @validator("ip")
    def validate_ip(cls, v):
        assert IP_REGXP.match(
            v) is not None, "ip must be a valid IPv4/IPv6 address"
        return v


# API
# outputs
BatchedSwitchOutput = batcheableOutputFactory(Switch)

# inputs


class UpsertSwitchInput(BaseModel):
    id: Optional[UUID4] = None
    ip: Optional[str] = None
    gpsLat: Optional[float] = None
    gpsLong: Optional[float] = None
    name: Optional[str] = None
    description: Optional[str] = None
    restricted: Optional[bool] = None
    restrictedPorts: Optional[list[int]] = None
    restrictedPortsDesc: Optional[list[str]] = None
