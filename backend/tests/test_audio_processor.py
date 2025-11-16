"""Audio processor tests"""
import pytest
from app.services.audio_processor import AudioProcessor
from app.utils.errors import AudioProcessingError

def test_audio_processor_initialization():
    """Test AudioProcessor can be instantiated"""
    processor = AudioProcessor()
    assert processor is not None

# Add more tests when sample audio files are available
