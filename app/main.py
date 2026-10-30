from fastapi import FastAPI
from app.api.banking import router as banking_router

app = FastAPI(title="SmartBank AI")

app.include_router(banking_router)



@app.get("/health")
def health_check():
    return{
        "status": "healthy",
        "service": "smartbank-ai"
    }

