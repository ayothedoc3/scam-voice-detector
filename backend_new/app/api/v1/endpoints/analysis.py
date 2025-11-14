from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.call_session import CallSession
from app.models.analysis_result import AnalysisResult
from app.core.security import get_current_user_id
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/history/{call_session_id}")
async def get_analysis_history(
    call_session_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get analysis history for a specific call session"""

    # Verify call session belongs to user
    result = await db.execute(
        select(CallSession).where(
            CallSession.id == call_session_id,
            CallSession.user_id == user_id
        )
    )
    call_session = result.scalar_one_or_none()

    if not call_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call session not found"
        )

    # Get all analysis results
    results = await db.execute(
        select(AnalysisResult)
        .where(AnalysisResult.call_session_id == call_session_id)
        .order_by(AnalysisResult.chunk_index)
    )
    analysis_results = results.scalars().all()

    return {
        "results": [
            {
                "id": r.id,
                "call_session_id": r.call_session_id,
                "chunk_index": r.chunk_index,
                "timestamp": r.timestamp.isoformat(),
                "risk_score": r.risk_score,
                "risk_level": r.risk_level,
                "is_deepfake": r.is_deepfake,
                "confidence": r.confidence,
                "transcript": r.transcript,
                "voice_characteristics": r.voice_characteristics
            }
            for r in analysis_results
        ]
    }


@router.get("/sessions")
async def get_call_sessions(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    limit: int = 20
):
    """Get all call sessions for the authenticated user"""

    results = await db.execute(
        select(CallSession)
        .where(CallSession.user_id == user_id)
        .order_by(CallSession.started_at.desc())
        .limit(limit)
    )
    sessions = results.scalars().all()

    return [
        {
            "id": s.id,
            "call_sid": s.call_sid,
            "status": s.status.value,
            "phone_number": s.phone_number,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            "total_duration": s.total_duration,
            "max_risk_score": s.max_risk_score,
            "final_verdict": s.final_verdict.value if s.final_verdict else None
        }
        for s in sessions
    ]
