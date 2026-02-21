from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import files
from core.config import settings
from core.logging import setup_logging
from core.request_id import RequestIDMiddleware
from core.database import get_db_pool
from core.minio_client import ensure_bucket_exists
import logging

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ensure_bucket_exists()                     # create MinIO bucket if missing
    pool = await get_db_pool()                  # create DB pool (also creates DB/table)
    app.state.db_pool = pool
    logger.info("Application started")
    yield
    # Shutdown
    await app.state.db_pool.close()
    logger.info("Application shut down")

app = FastAPI(title="File Storage API", version="1.0.0", lifespan=lifespan)

# Middleware
app.add_middleware(RequestIDMiddleware)

# Include routers
app.include_router(files.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)