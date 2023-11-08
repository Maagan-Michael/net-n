from sqlalchemy import Column, String, Integer
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .. import Base


class DBCustomer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    idstr = Column(String, index=True, unique=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    type = Column(String, index=True)
    address = Column(String, index=True)

    connections = relationship("DBConnection", back_populates="customer")
