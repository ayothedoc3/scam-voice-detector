"""Application configuration management"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    app_name: str = "Voice Scam Detector API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Resemble AI
    resemble_api_key: str
    resemble_api_url: str = "https://api.resemble.ai/v2/detect"

    # File Upload
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: set = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
    temp_upload_dir: str = "./temp_uploads"

    # CORS
    cors_origins: List[str] = ["*"]

    # Rate Limiting
    rate_limit_per_minute: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
