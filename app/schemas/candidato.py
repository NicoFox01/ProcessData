from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.enums import ProvinciaArgentina, NoticePeriod

class CandidatoBase(BaseModel):
    full_name: str
    linkedin_url: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    residence_area: Optional[ProvinciaArgentina] = None
    salary_expectations: Optional[int] = None
    notice_period: Optional[NoticePeriod] = None
    observations: Optional[str] = None

class CandidatoCreate(CandidatoBase):
    pass

class CandidatoUpdate(CandidatoBase):
    full_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    residence_area: Optional[ProvinciaArgentina] = None
    salary_expectations: Optional[int] = None
    notice_period: Optional[NoticePeriod] = None
    observations: Optional[str] = None

class CandidatoResponse(CandidatoBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 