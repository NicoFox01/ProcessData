from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.enums import TipoEmpresa

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