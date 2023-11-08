from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .. import Base


class DBCustomer(Base):
    __tablename__ = "customers"

    id = Column(UUID, primary_key=True, index=True, unique=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    type = Column(String, index=True)
    address = Column(String, index=True)

    connections = relationship("DBConnection", back_populates="customer")
