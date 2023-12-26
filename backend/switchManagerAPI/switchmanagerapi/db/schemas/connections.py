import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .. import Base
from .customers import DBCustomer
from .switches import DBSwitch


class DBConnection(Base):
    __tablename__ = "connections"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, unique=True, default=uuid.uuid4, nullable=False)
    name = Column(String, index=True, default=None, nullable=True)
    strPort = Column(String, index=True, default=None, nullable=False)
    port = Column(Integer, index=True, default=None, nullable=False)
    toggled = Column(Boolean, index=True, default=False, nullable=False)
    toggleDate = Column(DateTime, index=True, default=None, nullable=True)
    type = Column(String, index=True, default="copper|fiber", nullable=False)
    isUp = Column(Boolean, index=True, default=False, nullable=False)
    adapter = Column(String, index=True, default="imc|snmp", nullable=False)
    speed = Column(Integer, index=False, default=0, nullable=False)
    switchId = Column(UUID, ForeignKey("switches.id"),
                      index=True, default=None, nullable=False)
    customerId = Column(Integer, ForeignKey(
        "customers.id"), index=True, default=None, nullable=True)
    autoUpdate = Column(Boolean, index=True, default=True, nullable=False)
    address = Column(String, index=True, default=None, nullable=True)
    flat = Column(String, index=True, default=None, nullable=True)

    switch = relationship(
        "DBSwitch", back_populates="connections", foreign_keys=[switchId], order_by=DBSwitch.name.asc())
    customer = relationship(
        "DBCustomer", back_populates="connections", foreign_keys=[customerId], order_by=(DBCustomer.lastname.asc(), DBCustomer.firstname.asc()))
    UniqueConstraint(switchId, strPort, name="switch_port_unique")
