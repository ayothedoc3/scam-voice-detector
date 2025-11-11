"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .api import routes
from .utils.logger import setup_logging

settings = get_settings()
setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered voice deepfake detection API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router, prefix="/api/v1", tags=["detection"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    import os
    os.makedirs(settings.temp_upload_dir, exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)
