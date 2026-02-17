from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime, Enum, Column, ForeignKey, Boolean, Integer
from app.models.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.enums import TipoProceso, EstadoJob, Vertical
ARG = ZoneInfo("America/Argentina/Buenos_Aires")

class Job(Base):
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_name = Column(String(300), nullable=False, unique=True, index=True)
    empresa_id = Column(PG_UUID(as_uuid=True), ForeignKey("empresa.id"), nullable=False)
    cliente_id = Column(PG_UUID(as_uuid=True), ForeignKey("cliente.id"), nullable=False)
    opening_date = Column(DateTime(timezone=True), default=lambda: datetime.now(ARG))
    closing_date = Column(DateTime(timezone=True), nullable=True)
    vacancies = Column(Integer, default=1)
    state = Column(Enum(EstadoJob), default=EstadoJob.ABIERTA)
    type_of_process = Column(Enum(TipoProceso))
    vertical = Column(Enum(Vertical), nullable=False)

    
    empresa = relationship("Empresa", back_populates="job")
    cliente = relationship("Cliente", back_populates="job")
    procesos = relationship("Proceso", back_populates="job")
    templates = relationship("Template", back_populates="job")
