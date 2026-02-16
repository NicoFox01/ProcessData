from fastapi import APIRouter
from app.api.v1 import companies, clients
from app.api.v1.auth import login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])