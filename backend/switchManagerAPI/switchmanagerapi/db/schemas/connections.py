import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .. import Base
from sqlalchemy import event
from ...logger import get_logger


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

    switch = relationship(
        "DBSwitch", back_populates="connections", foreign_keys=[switchId])
    customer = relationship(
        "DBCustomer", back_populates="connections", foreign_keys=[customerId])
    UniqueConstraint(switchId, strPort, name="switch_port_unique")


logger = get_logger("connectionJobs")


@event.listens_for(DBConnection.port, 'modified', retval=True, propagate=True)
@event.listens_for(DBConnection.port, 'set', retval=True, propagate=True)
def validate_port(target, value, oldvalue, initiator):
    """validate port"""
    logger.info("here man")
    print("here man", flush=True)
    print([target, value, oldvalue], flush=True)
    return value


@event.listens_for(DBConnection.toggled, 'modified', retval=True, propagate=True)
@event.listens_for(DBConnection.toggled, 'set', retval=True, propagate=True)
def validate_toggle(target, value, oldvalue, initiator):
    logger.info("here man")
    """validate toggle"""
    print("here man", flush=True)
    print([target, value, oldvalue], flush=True)
    return value
