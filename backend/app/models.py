"""Pydantic models for request/response validation"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class SuspiciousSegment(BaseModel):
    """Model for suspicious audio segments"""
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")
    confidence: float = Field(..., ge=0, le=100, description="Confidence score")
    reason: str = Field(..., description="Why this segment is suspicious")
    features_detected: List[str] = Field(default=[], description="Specific features found")

class AudioMetadata(BaseModel):
    """Audio file metadata"""
    filename: str
    duration: float
    sample_rate: int
    channels: int
    bitrate: Optional[int] = None
    format: str

class DetectionResult(BaseModel):
    """Complete detection result"""
    is_deepfake: bool = Field(..., description="Whether deepfake was detected")
    confidence_score: float = Field(..., ge=0, le=100, description="Overall confidence")
    risk_level: str = Field(..., description="LOW, MEDIUM, HIGH, CRITICAL")
    explanation: str = Field(..., description="Human-readable explanation")
    suspicious_segments: List[SuspiciousSegment] = Field(default=[])
    audio_metadata: AudioMetadata
    detection_details: dict = Field(default={}, description="Raw API response")
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time_ms: float

    @field_validator('risk_level')
    @classmethod
    def validate_risk_level(cls, v):
        """Validate risk level values"""
        allowed = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        if v not in allowed:
            raise ValueError(f'risk_level must be one of {allowed}')
        return v

class AnalysisRequest(BaseModel):
    """Request model for analysis"""
    file_data: bytes
    filename: str
    enable_segment_analysis: bool = True
    sensitivity: str = "medium"  # low, medium, high

class BatchAnalysisResult(BaseModel):
    """Batch analysis results"""
    total_files: int
    processed: int
    failed: int
    results: List[DetectionResult]
    batch_id: str
    processing_time_total_ms: float
