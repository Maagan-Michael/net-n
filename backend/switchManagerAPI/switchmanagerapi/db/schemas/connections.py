import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .. import Base


class DBConnection(Base):
    __tablename__ = "connections"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, unique=True, default=uuid.uuid4)
    name = Column(String, index=True, default=None)
    strPort = Column(String, index=True)
    port = Column(Integer, index=True)
    toggled = Column(Boolean, index=True, default=False)
    toggleDate = Column(DateTime, index=True, default=None)
    type = Column(String, index=True, default="copper|fiber")
    isUp = Column(Boolean, index=True, default=False)
    adapter = Column(String, index=True, default="imc|snmp")
    speed = Column(Integer, index=False, default=0)
    switchId = Column(UUID, ForeignKey("switches.id"), index=True)
    customerId = Column(Integer, ForeignKey(
        "customers.id"), index=True, default=None)
    autoUpdate = Column(Boolean, index=True, default=True)
    address = Column(String, index=True, default=None)

    switch = relationship(
        "DBSwitch", back_populates="connections", foreign_keys=[switchId])
    customer = relationship(
        "DBCustomer", back_populates="connections", foreign_keys=[customerId])
    UniqueConstraint(switchId, strPort, name="switch_port_unique")
