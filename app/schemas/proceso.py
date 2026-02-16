from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.enums import EstadoGeneral

class ProcesoBase(BaseModel):
    job_id: UUID
    candidato_id:  UUID
    user_id: UUID
    state: EstadoGeneral = EstadoGeneral.SOURCING 
    substate_detail: Optional[str] = None
    feedback: Optional[str] = None

class ProcesoCreate(ProcesoBase):
    pass


class ProcesoUpdate(BaseModel): 
    state: Optional[EstadoGeneral] = None
    substate_detail: Optional[str] = None
    feedback: Optional[str] = None
    HR_interview: Optional[datetime] = None 
    CF_interview: Optional[datetime] = None
    client_interview: Optional[datetime] = None
    offer_interview: Optional[datetime] = None
    start_date: Optional[datetime] = None

class ProcesoResponse(ProcesoBase):
    id: UUID
    process_entry_date: datetime 
    HR_interview: Optional[datetime] = None 
    CF_interview: Optional[datetime] = None
    client_interview: Optional[datetime] = None
    offer_interview: Optional[datetime] = None
    start_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)