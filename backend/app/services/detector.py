"""Resemble AI API integration for deepfake detection"""
import os
import requests
import time
from typing import Dict, List
from ..config import get_settings
from ..models import DetectionResult, SuspiciousSegment, AudioMetadata
from ..utils.errors import DetectionAPIError
from ..utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

class ResembleDetector:
    """Interface with Resemble AI Detect API"""

    def __init__(self):
        self.api_key = settings.resemble_api_key
        self.api_url = settings.resemble_api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def detect_deepfake(self, audio_path: str) -> Dict:
        """Call Resemble AI API for deepfake detection"""
        try:
            # Upload file
            with open(audio_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    self.api_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files=files,
                    timeout=30
                )

            if response.status_code != 200:
                raise DetectionAPIError(f"API error: {response.status_code} - {response.text}")

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Resemble API request failed: {str(e)}")
            raise DetectionAPIError(f"Detection API failed: {str(e)}")

    def analyze_segments(self, audio_path: str, detection_result: Dict) -> List[SuspiciousSegment]:
        """Analyze audio segments for detailed suspicious patterns"""
        segments = []

        # Parse Resemble API response for segment data
        if 'segments' in detection_result:
            for seg in detection_result['segments']:
                segments.append(SuspiciousSegment(
                    start_time=seg.get('start', 0),
                    end_time=seg.get('end', 0),
                    confidence=seg.get('confidence', 0) * 100,
                    reason=seg.get('reason', 'Synthetic voice patterns detected'),
                    features_detected=seg.get('features', [])
                ))

        return segments

    def calculate_risk_level(self, confidence: float) -> str:
        """Determine risk level based on confidence score"""
        if confidence >= 90:
            return "CRITICAL"
        elif confidence >= 70:
            return "HIGH"
        elif confidence >= 50:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_explanation(self, detection_data: Dict, confidence: float) -> str:
        """Generate human-readable explanation"""
        if confidence >= 90:
            return (
                f"Very high confidence ({confidence:.1f}%) that this audio contains AI-generated voice. "
                "Multiple synthetic voice patterns detected across the recording. "
                "This is likely a deepfake scam attempt."
            )
        elif confidence >= 70:
            return (
                f"High confidence ({confidence:.1f}%) of AI-generated voice detected. "
                "Significant synthetic characteristics found. Exercise extreme caution."
            )
        elif confidence >= 50:
            return (
                f"Moderate confidence ({confidence:.1f}%) of potential deepfake. "
                "Some suspicious patterns detected. Verify through alternative means."
            )
        else:
            return (
                f"Low risk ({confidence:.1f}%). "
                "No significant synthetic voice patterns detected. Audio appears authentic."
            )
