from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from uuid import UUID

async def get_clients(db: AsyncSession):
    result = await db.execute(select(Cliente))
    return result.scalars().all()

async def get_client(db: AsyncSession, client_id: UUID):
    result = await db.execute(select(Cliente).where(Cliente.id == client_id))
    return result.scalar_one_or_none()

async def create_client(db: AsyncSession, client_in: ClienteCreate):
    db_company = Cliente(**client_in.model_dump())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def update_client(db: AsyncSession, client_id:UUID, client_in: ClienteUpdate):
    db_company = await get_client(db, client_id)
    if not db_company:
        return None
    update_data = client_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def delete_client(db: AsyncSession, client_id: UUID):
    db_client = await get_client(db, client_id)
    if not db_client:
        return None
    await db.delete(db_client)
    await db.commit()
    return True