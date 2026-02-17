from uuid import uuid4
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.enums import Vertical, TipoProceso

class Template(Base):
    __tablename__ = "templates"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    vertical: Mapped[Vertical] = mapped_column(Enum(Vertical), nullable=False)
    type_of_process: Mapped[TipoProceso] = mapped_column(Enum(TipoProceso), nullable=False)
    job_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=True)
    
    original_job = relationship("Job", foreign_keys=[job_id])
