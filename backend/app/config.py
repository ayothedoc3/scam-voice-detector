from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # App
    app_name: str = "Scam Shield API"
    app_version: str = "1.0.0"
    debug: bool = False
    app_domain: str = "localhost"
    app_url: str = "http://localhost:8000"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/scamshield"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret: str = "your-jwt-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # Resemble AI
    resemble_api_key: str = ""
    resemble_api_url: str = "https://api.resemble.ai/v2/detect"

    # VAPID (Web Push)
    vapid_public_key: str = ""
    vapid_private_key: str = ""
    vapid_email: str = ""

    # Storage
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "scamshield"

    # CORS
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # File Upload
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: set = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
