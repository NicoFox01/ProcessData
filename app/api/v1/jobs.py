from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, requiere_admin_or_selector, get_current_user, requiere_admin
from app.services.job_service import get_jobs, get_job, create_job, update_job, delete_job, create_job_by_template_id
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.models.enums import EstadoJob
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=list[JobResponse])
async def return_jobs(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await get_jobs(db)

@router.get("/{job_id}", response_model=JobResponse)
async def return_job_by_id(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await get_job(db, job_id)

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def new_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):
    return await create_job(db, job)


@router.post("/from-template", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def new_job_from_template(
    job_data: dict, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):      
    return await create_job_by_template_id(db, job_data)

@router.patch("/{job_id}/status", response_model=JobResponse)
async def modify_job_status(
    job_id: UUID, 
    status_data: dict, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin_or_selector)
):
    return await update_job(db, job_id, JobUpdate(**status_data))

@router.patch("/{job_id}/soft-delete", response_model=JobResponse)
async def soft_delete_job(
    job_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(requiere_admin)
):
    return await update_job(db, job_id, JobUpdate(state=EstadoJob.CANCELADA))
