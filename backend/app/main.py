from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.core.config import settings
from app.core.database import check_database_connection
from app.api.files import router as files_router
from app.api.requirements import (
    router as requirements_router,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="0.2.0",
    description="ReqLens API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    projects_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    files_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    requirements_router,
    prefix=settings.API_V1_PREFIX,
)




@app.get("/")
def root():
    return {
        "name": "ReqLens API",
        "version": "0.2.0",
        "status": "running",
    }


@app.get("/health")
def health():
    database_connected = check_database_connection()

    return {
        "status": "ok" if database_connected else "degraded",
        "database": "connected" if database_connected else "disconnected",
    }