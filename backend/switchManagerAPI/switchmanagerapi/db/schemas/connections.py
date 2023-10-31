from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .db import Base


class DBConnection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    port = Column(Integer, index=True)
    toggled = Column(Boolean, index=True)
    toggleDate = Column(DateTime, index=True)
    type = Column(String, index=True)
    isUp = Column(Boolean, index=True)
    adapter = Column(String, index=True)
    speed = Column(Integer, index=True)
    switchId = Column(Integer, ForeignKey("switches.id"), index=True)
    customerId = Column(Integer, ForeignKey("customers.id"), index=True)

    switch = relationship("DBSwitch", back_populates="connections")
    customer = relationship("DBCustomer", back_populates="connections")
