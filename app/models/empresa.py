from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime, Enum, Column
from app.models.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo
ARG = ZoneInfo("America/Argentina/Buenos_Aires")

class Empresa(Base):
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_name = Column(String(300), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ARG))
    
    cliente = relationship("Cliente", back_populates="empresa", cascade="all, delete-orphan")
    job = relationship("Job", back_populates="empresa", cascade="all, delete-orphan")