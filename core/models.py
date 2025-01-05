from sqlalchemy import Column, Index, Integer, String, Float, TIMESTAMP, func, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB

from .database import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    sensor_id = Column(String, index=True)
    human_presence = Column(Integer)
    dwell_time = Column(Float)
    timestamp = Column(TIMESTAMP(timezone=True), index=True)
    raw_data = Column(JSONB)

    __table_args__ = (
        PrimaryKeyConstraint("sensor_id", "timestamp"),
    )
