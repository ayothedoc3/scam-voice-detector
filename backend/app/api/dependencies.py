"""Dependency injection for API routes"""
from ..config import get_settings
from ..services.analyzer import VoiceAnalyzer

def get_analyzer() -> VoiceAnalyzer:
    """Get analyzer instance"""
    return VoiceAnalyzer()
