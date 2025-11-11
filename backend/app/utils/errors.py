"""Custom exception classes"""

class VoiceDetectorError(Exception):
    """Base exception for voice detector errors"""
    pass

class AudioProcessingError(VoiceDetectorError):
    """Raised when audio processing fails"""
    pass

class DetectionAPIError(VoiceDetectorError):
    """Raised when Resemble AI API calls fail"""
    pass

class FileValidationError(VoiceDetectorError):
    """Raised when file validation fails"""
    pass

class ConfigurationError(VoiceDetectorError):
    """Raised when configuration is invalid"""
    pass
