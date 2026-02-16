from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.enums import UserRole # Or simply remove line 5 if UserRole is not used in this file either. Let's just remove it since it's not used in the schema.

class EmpresaBase(BaseModel):
    company_name: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(EmpresaBase):
    company_name: Optional[str] = None

class EmpresaResponse(EmpresaBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 