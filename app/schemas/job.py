from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.enums import TipoProceso, EstadoJob, Vertical

class JobBase(BaseModel):
    job_name: str = Field(..., min_length=1)
    empresa_id: UUID
    cliente_id: UUID
    vacancies: int = Field(..., gt=0)
    state: EstadoJob = EstadoJob.ABIERTA
    type_of_process: TipoProceso
    vertical: Vertical

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    job_name: Optional[str] = None
    empresa_id: Optional[UUID] = None
    cliente_id: Optional[UUID] = None
    vacancies: Optional[int] = None
    state: Optional[EstadoJob] = None
    type_of_process: Optional[TipoProceso] = None
    vertical: Optional[Vertical] = None
    closing_date: Optional[datetime] = None

class JobResponse(JobBase):
    id: UUID
    opening_date: datetime
    closing_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True) 