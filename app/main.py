from fastapi import FastAPI

app = FastAPI(title = "SmartBank AI")


@app.get("/health")
def health_check():
    return{
        "status": "healthy",
        "service": "smartbank-ai"
    }

