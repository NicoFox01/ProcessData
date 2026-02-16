from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime, Enum, Column, ForeignKey
from app.models.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo
ARG = ZoneInfo("America/Argentina/Buenos_Aires")

class Cliente(Base):
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_name = Column(String(300), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ARG))
    empresa_id = Column(PG_UUID(as_uuid=True), ForeignKey("empresa.id"), nullable=False)
    
    empresa = relationship("Empresa", back_populates="cliente")
    job = relationship("Job", back_populates="cliente")
