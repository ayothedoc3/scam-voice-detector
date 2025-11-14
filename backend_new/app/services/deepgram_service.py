from deepgram import Deepgram
from app.core.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class DeepgramService:
    """Service for Deepgram speech-to-text"""

    def __init__(self):
        self.api_key = settings.DEEPGRAM_API_KEY
        self.client = Deepgram(self.api_key)

    async def transcribe_audio(self, audio_data: bytes) -> Optional[dict]:
        """
        Transcribe audio to text

        Args:
            audio_data: Audio file bytes

        Returns:
            Transcription result
        """
        try:
            source = {"buffer": audio_data, "mimetype": "audio/wav"}

            response = await self.client.transcription.prerecorded(
                source,
                {
                    "model": "nova-2",
                    "language": "en-US",
                    "punctuate": True,
                    "diarize": True,
                    "smart_format": True
                }
            )

            # Extract transcript
            if response and "results" in response:
                channels = response["results"]["channels"]
                if channels and len(channels) > 0:
                    alternatives = channels[0]["alternatives"]
                    if alternatives and len(alternatives) > 0:
                        transcript = alternatives[0]["transcript"]
                        confidence = alternatives[0].get("confidence", 0.0)

                        logger.info(f"Transcription complete: {len(transcript)} characters")

                        return {
                            "text": transcript,
                            "confidence": confidence,
                            "words": alternatives[0].get("words", [])
                        }

            logger.warning("No transcription results")
            return None

        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return None

    async def transcribe_stream(self, audio_stream):
        """
        Transcribe streaming audio (for real-time)

        Args:
            audio_stream: Audio stream generator

        Yields:
            Transcription updates
        """
        try:
            async def audio_generator():
                async for chunk in audio_stream:
                    yield chunk

            response = await self.client.transcription.live(
                {
                    "model": "nova-2",
                    "language": "en-US",
                    "punctuate": True,
                    "interim_results": True
                }
            )

            async for result in response:
                if "channel" in result:
                    transcript = result["channel"]["alternatives"][0]["transcript"]
                    if transcript:
                        yield {
                            "text": transcript,
                            "is_final": result.get("is_final", False)
                        }

        except Exception as e:
            logger.error(f"Stream transcription failed: {str(e)}")


# Singleton instance
deepgram_service = DeepgramService()
