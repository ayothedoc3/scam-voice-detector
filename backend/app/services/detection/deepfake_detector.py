import httpx
import tempfile
import os
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class DeepfakeDetector:
    """Integrates with Resemble AI for deepfake detection"""

    def __init__(self):
        self.api_key = settings.resemble_api_key
        self.api_url = settings.resemble_api_url
        if self.api_key:
            self.client = httpx.AsyncClient(
                timeout=30.0,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        else:
            logger.warning("Resemble AI API key not configured")
            self.client = None

    async def analyze(self, audio_data: bytes) -> dict:
        """
        Analyze audio for deepfake

        Returns:
            {
                'is_deepfake': bool,
                'confidence': float,
                'details': dict
            }
        """
        if not self.client:
            logger.warning("Resemble AI client not initialized, returning fallback result")
            return self._fallback_result()

        try:
            # Write to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name

            try:
                # Upload to Resemble AI
                with open(temp_path, 'rb') as f:
                    files = {'file': ('audio.wav', f, 'audio/wav')}
                    response = await self.client.post(self.api_url, files=files)

                if response.status_code != 200:
                    logger.error(f"Resemble API error: {response.status_code}")
                    return self._fallback_result()

                result = response.json()
                return {
                    'is_deepfake': result.get('is_deepfake', False),
                    'confidence': result.get('confidence', 0.0),
                    'details': result.get('details', {})
                }

            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        except Exception as e:
            logger.error(f"Deepfake detection error: {str(e)}")
            return self._fallback_result()

    def _fallback_result(self):
        """Fallback result if API fails"""
        return {
            'is_deepfake': False,
            'confidence': 0.0,
            'details': {},
            'error': True
        }

    async def close(self):
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()
