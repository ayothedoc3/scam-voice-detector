from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class CallStatus(str, enum.Enum):
    INITIALIZING = "initializing"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CallSession(Base):
    __tablename__ = "call_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    call_sid = Column(String, unique=True, index=True, nullable=False)
    stream_sid = Column(String, nullable=True)
    conference_sid = Column(String, nullable=True)
    status = Column(Enum(CallStatus), default=CallStatus.INITIALIZING)
    phone_number = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    total_duration = Column(Float, default=0.0)
    max_risk_score = Column(Float, default=0.0)
    final_verdict = Column(Enum(RiskLevel), nullable=True)

    # Relationships
    user = relationship("User", back_populates="call_sessions")
    analysis_results = relationship("AnalysisResult", back_populates="call_session", cascade="all, delete-orphan")
