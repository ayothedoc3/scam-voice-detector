from pydub import AudioSegment
import os

class AudioProcessor:
    """Handle audio file format conversion and preprocessing"""

    @staticmethod
    def convert_to_wav(input_path: str, output_path: str = None) -> str:
        """
        Convert audio file to WAV format

        Args:
            input_path: Path to input audio file
            output_path: Path for output WAV file (optional)

        Returns:
            Path to converted WAV file
        """
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}.wav"

        # Detect input format
        ext = os.path.splitext(input_path)[1].lower()

        if ext == '.mp3':
            audio = AudioSegment.from_mp3(input_path)
        elif ext == '.m4a':
            audio = AudioSegment.from_file(input_path, format='m4a')
        elif ext == '.wav':
            return input_path  # Already WAV
        else:
            raise ValueError(f"Unsupported audio format: {ext}")

        # Export as WAV
        audio.export(output_path, format='wav')
        return output_path

    @staticmethod
    def get_duration(audio_path: str) -> float:
        """Get audio duration in seconds"""
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0

    @staticmethod
    def validate_audio(audio_path: str, max_size_mb: int = 50) -> bool:
        """
        Validate audio file

        Args:
            audio_path: Path to audio file
            max_size_mb: Maximum file size in MB

        Returns:
            True if valid, raises exception otherwise
        """
        # Check file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Check file size
        file_size = os.path.getsize(audio_path)
        max_size_bytes = max_size_mb * 1024 * 1024

        if file_size > max_size_bytes:
            raise ValueError(f"File too large: {file_size} bytes (max: {max_size_bytes})")

        return True
