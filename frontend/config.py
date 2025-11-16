"""Frontend configuration"""
import os

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# App settings
APP_TITLE = "Voice Scam Detector"
APP_ICON = "🔊"

# File upload settings
MAX_FILE_SIZE_MB = 50
SUPPORTED_FORMATS = ['mp3', 'wav', 'm4a', 'ogg', 'flac']
