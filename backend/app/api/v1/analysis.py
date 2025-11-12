from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.models.call_session import CallSession
from app.models.analysis_result import AnalysisResult
from app.core.auth import get_current_user
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class AnalysisResultResponse(BaseModel):
    id: int
    chunk_index: int
    timestamp: datetime
    risk_score: float
    risk_level: str
    deepfake_data: dict
    voice_data: dict

    class Config:
        from_attributes = True


class CallSessionResponse(BaseModel):
    id: int
    call_sid: str
    status: str
    started_at: datetime
    ended_at: datetime | None
    total_duration: float
    max_risk_score: float
    final_verdict: str | None

    class Config:
        from_attributes = True


@router.get("/sessions", response_model=List[CallSessionResponse])
async def get_call_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """Get user's call sessions"""
    result = await db.execute(
        select(CallSession)
        .where(CallSession.user_id == current_user.id)
        .order_by(CallSession.started_at.desc())
        .offset(skip)
        .limit(limit)
    )
    sessions = result.scalars().all()
    return sessions


@router.get("/sessions/{session_id}", response_model=CallSessionResponse)
async def get_call_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific call session"""
    result = await db.execute(
        select(CallSession)
        .where(CallSession.id == session_id, CallSession.user_id == current_user.id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Call session not found")

    return session


@router.get("/sessions/{session_id}/results", response_model=List[AnalysisResultResponse])
async def get_session_results(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analysis results for a call session"""
    # Verify session belongs to user
    session_result = await db.execute(
        select(CallSession)
        .where(CallSession.id == session_id, CallSession.user_id == current_user.id)
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Call session not found")

    # Get analysis results
    results = await db.execute(
        select(AnalysisResult)
        .where(AnalysisResult.call_session_id == session_id)
        .order_by(AnalysisResult.timestamp.asc())
    )
    analysis_results = results.scalars().all()

    return analysis_results
