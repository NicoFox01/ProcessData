from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime, Enum, Column, ForeignKey
from app.models.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo
ARG = ZoneInfo("America/Argentina/Buenos_Aires")
from app.models.enums import EstadoGeneral

class Proceso(Base):
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id = Column(PG_UUID(as_uuid=True), ForeignKey("job.id"), nullable=False)
    candidato_id = Column(PG_UUID(as_uuid=True), ForeignKey("candidato.id"), nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    state = Column(Enum(EstadoGeneral), default=EstadoGeneral.SOURCING)
    substate_detail = Column(String(50), nullable=True)
    process_entry_date = Column(DateTime(timezone=True), default=lambda: datetime.now(ARG))
    HR_interview = Column(DateTime(timezone=True), nullable=True)
    feedback = Column(String(1000), nullable=True)

    candidato = relationship("Candidato", back_populates="procesos")
    job = relationship("Job", back_populates="procesos")
    user = relationship("User", back_populates="procesos")