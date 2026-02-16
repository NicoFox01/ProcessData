from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, requiere_admin
from app.services.company_service import get_companies, get_company, create_company, update_company, delete_company
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from uuid import UUID
from app.models.enums import UserRole
router = APIRouter()

@router.get("/", response_model=list[EmpresaResponse])
async def read_companies(db: AsyncSession = Depends(get_db)):
    return await get_companies(db)

@router.get("/{company_id}", response_model=EmpresaResponse)
async def read_company(company_id: UUID, db: AsyncSession = Depends(get_db)):
    company = await get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
async def new_company(
    company_in: EmpresaCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin)
):
    return await create_company(db, company_in)
    

@router.put("/{company_id}", response_model=EmpresaResponse)
async def modify_company(
    company_id: UUID,
    company_in: EmpresaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin)
):
    company = await update_company(db, company_id, company_in)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin)
):
    success = await delete_company(db, company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return None