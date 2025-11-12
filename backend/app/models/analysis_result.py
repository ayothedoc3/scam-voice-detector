from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    call_session_id = Column(Integer, ForeignKey("call_sessions.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL

    # Detection data
    deepfake_data = Column(JSON)
    transcript_data = Column(JSON)
    voice_data = Column(JSON)
    scam_indicators = Column(JSON)

    # Relationships
    call_session = relationship("CallSession", back_populates="analysis_results")
