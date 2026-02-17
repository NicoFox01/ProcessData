from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from app.models.enums import Vertical, TipoProceso

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    vertical: Vertical
    type_of_process: TipoProceso

class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    vertical: Optional[Vertical] = None
    type_of_process: Optional[TipoProceso] = None
    job_id: Optional[UUID] = None

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    vertical: Optional[Vertical] = None
    type_of_process: Optional[TipoProceso] = None
    job_id: Optional[UUID] = None

class TemplateResponse(TemplateBase):
    id: UUID
    job_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)
