
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.resources import router as resources_router
from app.api.incidents import router as incidents_router
from app.database import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Riverine Flood Disaster Management System",
    description="Multi-agent decision support for flood emergencies.",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(incidents_router)
app.include_router(resources_router)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "riverine-flood-management",
        "version": "0.2.0",
    }
