from fastapi import FastAPI
from mangum import Mangum
from app.api.api import api_router
from app.core.config import settings
app = FastAPI(title="PD-BE Serverless API")

@app.get("/")
def read_root():
    return {"message": "Hello World from PD-BE Serverless!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Handler para AWS Lambda / Vercel
handler = Mangum(app)

app.include_router(api_router, prefix=settings.API_VERSION)