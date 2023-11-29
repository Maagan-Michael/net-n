from sqlalchemy import Float, Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .. import Base


class DBSwitch(Base):
    __tablename__ = "switches"

    id = Column(UUID, primary_key=True, index=True, unique=True)
    ip = Column(String, index=False)
    gpsLat = Column(Float, index=True)
    gpsLong = Column(Float, index=True)
    name = Column(String, index=True)
    description = Column(String, index=False)
    restricted = Column(Boolean, index=True, default=False)
    notReachable = Column(Boolean, index=True, default=False)

    connections = relationship("DBConnection", back_populates="switch")
