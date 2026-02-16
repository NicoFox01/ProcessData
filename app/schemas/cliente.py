from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ClienteBase(BaseModel):
    client_name: str
    empresa_id: UUID

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    client_name: Optional[str] = None
    empresa_id: Optional[UUID] = None

class ClienteResponse(ClienteBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 
