from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate
from uuid import UUID
from app.services.template_service import get_template_by_id
from fastapi import HTTPException

async def get_jobs(db: AsyncSession):
    result = await db.execute(select(Job))
    return result.scalars().all()

async def get_job(db: AsyncSession, job_id: UUID):
    result = await db.execute(select(Job).where(Job.id == job_id))
    return result.scalar_one_or_none()

async def create_job(db: AsyncSession, job_in: JobCreate):
    data = job_in.model_dump()
    if isinstance(data.get("empresa_id"), str):
        data["empresa_id"] = UUID(data["empresa_id"])
    if isinstance(data.get("cliente_id"), str):
        data["cliente_id"] = UUID(data["cliente_id"])
        
    db_job = Job(**data)
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

from app.models.template import Template

async def create_job_by_template_id(db: AsyncSession, job_data: dict):
    template_id = job_data.get("template_id")
    if isinstance(template_id, str):
        template_id = UUID(template_id)
    
    result = await db.execute(select(Template).where(Template.id == template_id))
    template = result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    new_job_data = job_data.copy()
    new_job_data.pop("template_id", None)

    if isinstance(new_job_data.get("empresa_id"), str):
        new_job_data["empresa_id"] = UUID(new_job_data["empresa_id"])
    if isinstance(new_job_data.get("cliente_id"), str):
        new_job_data["cliente_id"] = UUID(new_job_data["cliente_id"])

    new_job_data["vertical"] = template.vertical
    new_job_data["type_of_process"] = template.type_of_process
    
    db_job = Job(**new_job_data)
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

async def update_job(db: AsyncSession, job_id: UUID, job_in: JobUpdate):
    db_job = await get_job(db, job_id)
    if not db_job:
        return None
    update_data = job_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    await db.commit()
    await db.refresh(db_job)
    return db_job

async def delete_job(db: AsyncSession, job_id: UUID):
    db_job = await get_job(db, job_id)
    if not db_job:
        return None
    await db.delete(db_job)
    await db.commit()
    return True