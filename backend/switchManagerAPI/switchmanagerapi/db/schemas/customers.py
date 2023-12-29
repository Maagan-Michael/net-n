from sqlalchemy import Column, String, Integer
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .. import Base


class DBCustomer(Base):
    """
        DBCustomer is the database model for a customer entry.
        id is the id of the customer (A.K.A customer work id)
        idstr is the string representation of the id
        firstname is the firstname of the customer
        lastname is the lastname of the customer
        type is the type of the customer (private/company)
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    idstr = Column(String, index=True, unique=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    type = Column(String, index=True)

    connections = relationship("DBConnection", back_populates="customer")
