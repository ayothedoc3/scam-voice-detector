from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.db.session import engine, Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    # Startup
    logger.info("Starting Scam Shield API...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")
    yield
    # Shutdown
    logger.info("Shutting down Scam Shield API...")
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api.v1 import auth, protection, analysis, twilio, upload
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(protection.router, prefix="/api/v1/protection", tags=["protection"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["upload"])
app.include_router(twilio.router, prefix="/api/v1/twilio", tags=["twilio"])

# Mount Socket.IO
from app.websocket.server import sio_app
app.mount("/socket.io", sio_app)


@app.get("/")
def root():
    return {
        "message": "Scam Shield API",
        "version": settings.app_version,
        "status": "operational"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.app_version
    }
