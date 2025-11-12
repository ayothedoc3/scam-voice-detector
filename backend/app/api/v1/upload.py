from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.core.auth import get_current_user
from app.config import get_settings
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


class UploadResponse(BaseModel):
    message: str
    file_id: str
    risk_score: float
    risk_level: str


@router.post("/audio", response_model=UploadResponse)
async def upload_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload audio file for analysis

    Accepts audio files and performs deepfake detection
    """
    # Validate file extension
    file_extension = f".{file.filename.split('.')[-1].lower()}"
    if file_extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.allowed_extensions)}"
        )

    # Read file
    content = await file.read()

    # Validate file size
    if len(content) > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.max_file_size / 1024 / 1024}MB"
        )

    try:
        # Analyze audio
        from app.services.detection.deepfake_detector import DeepfakeDetector
        from app.services.audio.analyzer import VoiceAnalyzer

        deepfake_detector = DeepfakeDetector()
        voice_analyzer = VoiceAnalyzer()

        deepfake_result = await deepfake_detector.analyze(content)
        voice_result = await voice_analyzer.analyze(content)

        # Calculate risk score
        risk_score = 0.0
        if deepfake_result.get('confidence'):
            risk_score += deepfake_result['confidence'] * 70
        if voice_result.get('synthetic_score'):
            risk_score += voice_result['synthetic_score'] * 0.3

        risk_score = min(risk_score, 100.0)

        # Determine risk level
        if risk_score >= 86:
            risk_level = 'CRITICAL'
        elif risk_score >= 61:
            risk_level = 'HIGH'
        elif risk_score >= 31:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return UploadResponse(
            message="Analysis complete",
            file_id=file.filename,
            risk_score=risk_score,
            risk_level=risk_level
        )

    except Exception as e:
        logger.error(f"Upload analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
