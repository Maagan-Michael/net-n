from typing import List
from sqlalchemy import Float, Column, String, Boolean, Integer, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from .. import Base
import uuid


class DBSwitch(Base):
    __tablename__ = "switches"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,
                unique=True, default=uuid.uuid4)
    ip = Column(String, index=False)
    gpsLat = Column(Float, index=True)
    gpsLong = Column(Float, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=False)
    restricted = Column(Boolean, index=True, default=False)
    notReachable = Column(Boolean, index=True, default=False)
    restrictedPorts = Column(ARRAY(Integer), index=False)
    restrictedPortsDesc = Column(ARRAY(String), index=False)

    connections: Mapped[List["DBConnection"]] = relationship(
        "DBConnection", back_populates="switch")
