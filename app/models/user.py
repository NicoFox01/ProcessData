from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime, Enum, Column, ForeignKey, Boolean
from app.models.base import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.enums import UserRole, Vertical
ARG = ZoneInfo("America/Argentina/Buenos_Aires")

class User(Base):
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(300), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.SELECTOR)
    vertical = Column(Enum(Vertical), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ARG))

    procesos = relationship("Proceso", back_populates="user")
    
