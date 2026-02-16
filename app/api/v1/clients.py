from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, requiere_admin
from app.services.client_service import get_clients, get_client, create_client, update_client, delete_client
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from uuid import UUID
from app.services.company_service import get_company

router = APIRouter()

@router.get("/", response_model=list[ClienteResponse])
async def read_clients(db: AsyncSession = Depends(get_db)):
    return await get_clients(db)

@router.get("/{client_id}", response_model=ClienteResponse)
async def read_client(client_id: UUID, db: AsyncSession = Depends(get_db)):
    client = await get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def new_client(
    client_in: ClienteCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin)
):
    empresa = await get_company(db, client_in.empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Company not found")
    return await create_client(db, client_in)

@router.put("/{client_id}", response_model=ClienteResponse)
async def modify_client(
    client_id: UUID,
    client_in: ClienteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin)
):
    client = await update_client(db, client_id, client_in)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin)
):
    success = await delete_client(db, client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return None