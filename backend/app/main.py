from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import check_database_connection



app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="ReqLens API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "ReqLens API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    database_connected = check_database_connection()

    return {
        "status": "ok" if database_connected else "degraded",
        "database": "connected" if database_connected else "disconnected",
    }