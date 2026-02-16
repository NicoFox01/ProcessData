from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate
from uuid import UUID

async def get_companies(db: AsyncSession):
    result = await db.execute(select(Empresa))
    return result.scalars().all()

async def get_company(db: AsyncSession, company_id: UUID):
    result = await db.execute(select(Empresa).where(Empresa.id == company_id))
    return result.scalar_one_or_none()

async def create_company(db: AsyncSession, company_in: EmpresaCreate):
    db_company = Empresa(**company_in.model_dump())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def update_company(db: AsyncSession, company_id: UUID, company_in: EmpresaUpdate):
    db_company = await get_company(db, company_id)
    if not db_company:
        return None
    update_data = company_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def delete_company(db: AsyncSession, company_id: UUID):
    db_company = await get_company(db, company_id)
    if not db_company:
        return None
    await db.delete(db_company)
    await db.commit()
    return True