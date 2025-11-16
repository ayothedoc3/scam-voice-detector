"""Audio file preprocessing and validation"""
import os
import tempfile
import librosa
import soundfile as sf
from pydub import AudioSegment
from typing import Tuple, Optional
from ..models import AudioMetadata
from ..utils.errors import AudioProcessingError

class AudioProcessor:
    """Handle audio file preprocessing and validation"""

    @staticmethod
    def validate_audio(file_path: str, max_duration: int = 600) -> bool:
        """Validate audio file is processable"""
        try:
            audio_info = AudioProcessor.get_metadata(file_path)
            if audio_info.duration > max_duration:
                raise AudioProcessingError(f"Audio too long: {audio_info.duration}s (max {max_duration}s)")
            return True
        except Exception as e:
            raise AudioProcessingError(f"Invalid audio file: {str(e)}")

    @staticmethod
    def get_metadata(file_path: str) -> AudioMetadata:
        """Extract audio metadata"""
        try:
            y, sr = librosa.load(file_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)

            # Get additional info using pydub
            audio = AudioSegment.from_file(file_path)

            return AudioMetadata(
                filename=os.path.basename(file_path),
                duration=duration,
                sample_rate=sr,
                channels=audio.channels,
                bitrate=audio.frame_rate,
                format=file_path.split('.')[-1]
            )
        except Exception as e:
            raise AudioProcessingError(f"Failed to extract metadata: {str(e)}")

    @staticmethod
    def normalize_audio(file_path: str, target_sr: int = 16000) -> str:
        """Normalize audio for better detection"""
        try:
            # Load and resample
            y, sr = librosa.load(file_path, sr=target_sr)

            # Normalize volume
            y = librosa.util.normalize(y)

            # Save normalized version
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            sf.write(temp_file.name, y, target_sr)

            return temp_file.name
        except Exception as e:
            raise AudioProcessingError(f"Audio normalization failed: {str(e)}")

    @staticmethod
    def convert_to_wav(file_path: str) -> str:
        """Convert audio to WAV format for API compatibility"""
        try:
            audio = AudioSegment.from_file(file_path)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio.export(temp_file.name, format='wav')
            return temp_file.name
        except Exception as e:
            raise AudioProcessingError(f"Format conversion failed: {str(e)}")
