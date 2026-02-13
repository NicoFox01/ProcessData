from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="PD-BE Serverless API")

@app.get("/")
def read_root():
    return {"message": "Hello World from PD-BE Serverless!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Handler para AWS Lambda / Vercel
handler = Mangum(app)
