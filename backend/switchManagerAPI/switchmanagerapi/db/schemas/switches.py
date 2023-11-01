from sqlalchemy import Float, Column, Integer, String
from sqlalchemy.orm import relationship
from .. import Base


class DBSwitch(Base):
    __tablename__ = "switches"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=False)
    gpsLat = Column(Float, index=True)
    gpsLong = Column(Float, index=True)
    name = Column(String, index=True)
    description = Column(String, index=False)

    connections = relationship("DBConnection", back_populates="switch")
