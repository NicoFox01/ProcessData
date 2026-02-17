from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, requiere_admin_or_selector, get_current_user
# Usamos un alias (as) para que no se llamen igual que los endpoints
from app.services.template_service import get_templates, get_template_by_id, create_template, update_template, delete_template
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse
from uuid import UUID
from fastapi import HTTPException

router = APIRouter()

@router.get("/", response_model=list[TemplateResponse])
async def return_templates(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):
    return await get_templates(db)

@router.get("/{template_id}", response_model=TemplateResponse)
async def return_template_by_id(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):
    return await get_template_by_id(db, template_id)

@router.post("/", response_model=TemplateResponse, status_code = status.HTTP_201_CREATED)
async def new_template(
    template: TemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):
    return await create_template(db, template)

@router.put("/{template_id}", response_model=TemplateResponse, status_code = status.HTTP_201_CREATED)
async def modify_template(
    template_id: UUID,
    template: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):
    return await update_template(template_id, template, db)

@router.delete("/{template_id}", response_model=TemplateResponse)
async def remove_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):
    return await delete_template(template_id, db)

