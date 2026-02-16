from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime, Enum, Column, ForeignKey, Boolean, Integer
from app.models.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.enums import ProvinciaArgentina, NoticePeriod
ARG = ZoneInfo("America/Argentina/Buenos_Aires")

class Candidato(Base):
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_name = Column(String(300), nullable=False, unique=True, index=True)
    linkedin_url = Column(String(300), nullable=False, unique=True, index=True)
    email = Column(String(300), nullable=True, unique=True, index=True)
    phone = Column(String(300), nullable=True, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ARG))
    residence_area = Column(Enum(ProvinciaArgentina), nullable=True)
    salary_expectations = Column(Integer, nullable=True)
    notice_period = Column(Enum(NoticePeriod), nullable=True)
    observations = Column(String(1000), nullable=True)

    procesos = relationship("Proceso", back_populates="candidato")