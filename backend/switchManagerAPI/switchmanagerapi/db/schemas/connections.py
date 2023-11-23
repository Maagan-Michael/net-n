from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .. import Base


class DBConnection(Base):
    __tablename__ = "connections"

    id = Column(UUID, primary_key=True, index=True, unique=True)
    name = Column(String, index=True, unique=True)
    strPort = Column(String, index=True)
    port = Column(Integer, index=True)
    toggled = Column(Boolean, index=True)
    toggleDate = Column(DateTime, index=True)
    type = Column(String, index=True)
    isUp = Column(Boolean, index=True)
    adapter = Column(String, index=True)
    speed = Column(Integer, index=False)
    switchId = Column(UUID, ForeignKey("switches.id"), index=True)
    customerId = Column(Integer, ForeignKey("customers.id"), index=True)
    autoUpdate = Column(Boolean, index=True, default=True)

    switch = relationship(
        "DBSwitch", back_populates="connections", foreign_keys=[switchId])
    customer = relationship(
        "DBCustomer", back_populates="connections", foreign_keys=[customerId])
