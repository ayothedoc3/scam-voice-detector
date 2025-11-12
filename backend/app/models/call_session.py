from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class CallSession(Base):
    __tablename__ = "call_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    call_sid = Column(String, unique=True, index=True, nullable=False)
    stream_sid = Column(String, unique=True, index=True)
    status = Column(String, default="active")  # active, completed, failed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    total_duration = Column(Float, default=0.0)
    max_risk_score = Column(Float, default=0.0)
    final_verdict = Column(String)  # LOW, MEDIUM, HIGH, CRITICAL
    notes = Column(Text)

    # Relationships
    user = relationship("User", back_populates="call_sessions")
    analysis_results = relationship("AnalysisResult", back_populates="call_session", cascade="all, delete-orphan")
