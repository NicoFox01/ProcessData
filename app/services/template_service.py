from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate
from uuid import UUID

async def get_templates(db: AsyncSession):
    result = await db.execute(select(Template))
    return result.scalars().all()

async def get_template_by_id(db: AsyncSession, template_id: UUID) -> Template | None:
    result = await db.execute(select(Template).where(Template.id == template_id))
    return result.scalar_one_or_none()

from app.models.job import Job

async def create_template(db: AsyncSession, template_in: TemplateCreate) -> Template:
    vertical = template_in.vertical
    process = template_in.type_of_process

    if template_in.job_id:
        job_result = await db.execute(select(Job).where(Job.id == template_in.job_id))
        job = job_result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=404, detail="Job source not found")
        vertical = job.vertical
        process = job.type_of_process

    db_template = Template(
        name=template_in.name,
        description=template_in.description,
        vertical=vertical,
        type_of_process=process,
        job_id=template_in.job_id
    )
    db.add(db_template)
    await db.commit()
    await db.refresh(db_template)
    return db_template

async def update_template(db: AsyncSession, template_id: UUID, template_in: TemplateUpdate) -> Template | None:
    db_template = await get_template_by_id(db, template_id)
    if not db_template:
        return None
    update_data = template_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "vertical" or field == "type_of_process":
            continue
        setattr(db_template, field, value)
    await db.commit()
    await db.refresh(db_template)
    return db_template

async def delete_template(db: AsyncSession, template_id: UUID) -> Template | None:
    db_template = await get_template_by_id(db, template_id)
    if not db_template:
        return None
    await db.delete(db_template)
    await db.commit()
    return db_template

