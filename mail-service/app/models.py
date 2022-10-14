from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType, JSONType
from datetime import datetime

from .database import Base


class Events(Base):
    __tablename__ = "received_events"

    id = Column(String, primary_key=True, index=True)
    value = Column(JSONType)
    treated = Column(Boolean, default=False)
    treated_at = Column(DateTime(timezone=True), nullable=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
