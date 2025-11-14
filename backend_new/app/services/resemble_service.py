import httpx
from app.core.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ResembleService:
    """Service for Resemble AI deepfake detection"""

    def __init__(self):
        self.api_key = settings.RESEMBLE_API_KEY
        self.base_url = "https://app.resemble.ai/api/v2"
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    async def detect_deepfake(self, audio_data: bytes) -> Optional[dict]:
        """
        Detect if audio is AI-generated/deepfake

        Args:
            audio_data: Audio file bytes

        Returns:
            Detection result with confidence score
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Upload audio for analysis
                files = {"file": ("audio.wav", audio_data, "audio/wav")}

                response = await client.post(
                    f"{self.base_url}/detect",
                    headers={"Authorization": f"Token {self.api_key}"},
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()

                    # Extract detection data
                    is_deepfake = result.get("is_deepfake", False)
                    confidence = result.get("confidence", 0.0)

                    logger.info(f"Deepfake detection: {is_deepfake} (confidence: {confidence})")

                    return {
                        "is_deepfake": is_deepfake,
                        "confidence": confidence,
                        "details": result.get("details", {})
                    }
                else:
                    logger.error(f"Resemble API error: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"Deepfake detection failed: {str(e)}")
            return None

    async def analyze_voice_characteristics(self, audio_data: bytes) -> Optional[dict]:
        """
        Analyze voice characteristics for synthetic indicators

        Args:
            audio_data: Audio file bytes

        Returns:
            Voice analysis results
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"file": ("audio.wav", audio_data, "audio/wav")}

                response = await client.post(
                    f"{self.base_url}/voice/analyze",
                    headers={"Authorization": f"Token {self.api_key}"},
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()

                    return {
                        "synthetic_score": result.get("synthetic_score", 0.0),
                        "pitch_mean": result.get("pitch_mean", 0.0),
                        "pitch_std": result.get("pitch_std", 0.0),
                        "spectral_centroid": result.get("spectral_centroid", 0.0)
                    }
                else:
                    logger.error(f"Voice analysis error: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"Voice analysis failed: {str(e)}")
            return None


# Singleton instance
resemble_service = ResembleService()
