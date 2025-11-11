"""Main analysis orchestrator"""
import time
from typing import Tuple
from ..models import DetectionResult, AudioMetadata
from ..services.detector import ResembleDetector
from ..services.audio_processor import AudioProcessor
from ..utils.logger import get_logger

logger = get_logger(__name__)

class VoiceAnalyzer:
    """Main analysis orchestrator"""

    def __init__(self):
        self.detector = ResembleDetector()
        self.processor = AudioProcessor()

    def analyze_audio(self, audio_path: str) -> DetectionResult:
        """Complete analysis pipeline"""
        start_time = time.time()

        try:
            # Step 1: Validate and get metadata
            logger.info(f"Analyzing audio: {audio_path}")
            self.processor.validate_audio(audio_path)
            metadata = self.processor.get_metadata(audio_path)

            # Step 2: Normalize audio for better detection
            normalized_path = self.processor.normalize_audio(audio_path)

            # Step 3: Run detection
            detection_data = self.detector.detect_deepfake(normalized_path)

            # Step 4: Parse results
            is_deepfake = detection_data.get('is_deepfake', False)
            confidence = detection_data.get('confidence', 0) * 100  # Convert to percentage

            # Step 5: Analyze segments
            segments = self.detector.analyze_segments(normalized_path, detection_data)

            # Step 6: Calculate risk and explanation
            risk_level = self.detector.calculate_risk_level(confidence)
            explanation = self.detector.generate_explanation(detection_data, confidence)

            processing_time = (time.time() - start_time) * 1000  # Convert to ms

            return DetectionResult(
                is_deepfake=is_deepfake,
                confidence_score=confidence,
                risk_level=risk_level,
                explanation=explanation,
                suspicious_segments=segments,
                audio_metadata=metadata,
                detection_details=detection_data,
                processing_time_ms=processing_time
            )

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise
