import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for the backend"""

    RESEMBLE_API_KEY = os.getenv("RESEMBLE_API_KEY")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

    # Audio settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = ['.mp3', '.wav', '.m4a']

    # API settings
    API_TIMEOUT = 30  # seconds

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.RESEMBLE_API_KEY:
            raise ValueError("RESEMBLE_API_KEY not set in environment")
