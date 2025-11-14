from app.services.resemble_service import resemble_service
from app.services.deepgram_service import deepgram_service
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analyzing audio chunks"""

    def __init__(self):
        self.resemble = resemble_service
        self.deepgram = deepgram_service

    async def analyze_audio_chunk(self, audio_data: bytes, chunk_index: int) -> dict:
        """
        Perform comprehensive analysis on an audio chunk

        Args:
            audio_data: Audio bytes
            chunk_index: Index of the chunk in the call

        Returns:
            Complete analysis result
        """
        logger.info(f"Analyzing chunk {chunk_index}")

        # Run analyses in parallel
        deepfake_result = await self.resemble.detect_deepfake(audio_data)
        voice_chars = await self.resemble.analyze_voice_characteristics(audio_data)
        transcript = await self.deepgram.transcribe_audio(audio_data)

        # Calculate risk score
        risk_score = self._calculate_risk_score(
            deepfake_result,
            voice_chars,
            transcript
        )

        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)

        return {
            "chunk_index": chunk_index,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "deepfake": deepfake_result or {"is_deepfake": False, "confidence": 0.0},
            "voice": voice_chars or {},
            "transcript": transcript or {"text": "", "confidence": 0.0}
        }

    def _calculate_risk_score(
        self,
        deepfake_result: Optional[dict],
        voice_chars: Optional[dict],
        transcript: Optional[dict]
    ) -> float:
        """
        Calculate overall risk score from analysis results

        Returns:
            Risk score from 0-100
        """
        score = 0.0

        # Deepfake detection (60% weight)
        if deepfake_result and deepfake_result.get("is_deepfake"):
            deepfake_confidence = deepfake_result.get("confidence", 0.0)
            score += deepfake_confidence * 60

        # Voice characteristics (30% weight)
        if voice_chars:
            synthetic_score = voice_chars.get("synthetic_score", 0.0)
            score += synthetic_score * 30

        # Transcript analysis (10% weight)
        # Could add keyword/sentiment analysis here
        if transcript:
            text = transcript.get("text", "").lower()
            # Check for common scam keywords
            scam_keywords = [
                "verify", "account", "suspended", "urgent", "immediate",
                "security", "payment", "refund", "irs", "social security",
                "winner", "prize", "congratulations", "claim"
            ]
            keyword_matches = sum(1 for keyword in scam_keywords if keyword in text)
            keyword_score = min(keyword_matches * 2.5, 10)  # Max 10 points
            score += keyword_score

        return min(score, 100.0)

    def _determine_risk_level(self, risk_score: float) -> str:
        """
        Determine risk level based on score

        Args:
            risk_score: Score from 0-100

        Returns:
            Risk level: LOW, MEDIUM, HIGH, or CRITICAL
        """
        if risk_score >= 70:
            return "CRITICAL"
        elif risk_score >= 50:
            return "HIGH"
        elif risk_score >= 30:
            return "MEDIUM"
        else:
            return "LOW"


# Singleton instance
analysis_service = AnalysisService()
