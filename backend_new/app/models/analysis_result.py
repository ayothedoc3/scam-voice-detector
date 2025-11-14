from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    call_session_id = Column(Integer, ForeignKey("call_sessions.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    is_deepfake = Column(Boolean, default=False)
    confidence = Column(Float, nullable=False)
    transcript = Column(String, nullable=True)
    voice_characteristics = Column(JSON, nullable=True)

    # Relationships
    call_session = relationship("CallSession", back_populates="analysis_results")
