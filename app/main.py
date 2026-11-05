from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.banking import router as banking_router
from app.api.auth import router as auth_router


app = FastAPI(title="SmartBank AI")

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(banking_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "smartbank-ai"
    }