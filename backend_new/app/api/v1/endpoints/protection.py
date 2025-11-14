from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.call_session import CallSession, CallStatus
from app.schemas.protection import (
    StartProtectionRequest,
    StartProtectionResponse,
    StopProtectionRequest,
    CallStatusResponse
)
from app.core.security import get_current_user_id
from app.services.twilio_service import twilio_service
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/start", response_model=StartProtectionResponse)
async def start_protection(
    request: StartProtectionRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Start call protection for a user"""

    # Create new call session
    call_session = CallSession(
        user_id=user_id,
        call_sid="pending",  # Will be updated when call is created
        status=CallStatus.INITIALIZING,
        phone_number=request.user_phone
    )

    db.add(call_session)
    await db.commit()
    await db.refresh(call_session)

    # Initiate Twilio call
    try:
        call_data = twilio_service.create_protection_call(
            to_number=request.user_phone,
            call_session_id=call_session.id
        )

        # Update call session with call SID
        call_session.call_sid = call_data["call_sid"]
        await db.commit()

        logger.info(f"Protection started for user {user_id}, session {call_session.id}")

        return StartProtectionResponse(
            session_id=call_session.id,
            call_sid=call_data["call_sid"],
            bridge_number=settings.TWILIO_PHONE_NUMBER,
            instructions=(
                "1. Answer the incoming call from Scam Shield\n"
                "2. Tap 'Add Call' and dial the suspicious number\n"
                "3. Once connected, tap 'Merge Calls'\n"
                "4. We'll analyze the conversation in real-time"
            )
        )

    except Exception as e:
        logger.error(f"Failed to start protection: {str(e)}")

        # Update session status to failed
        call_session.status = CallStatus.FAILED
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate protection call: {str(e)}"
        )


@router.post("/stop")
async def stop_protection(
    request: StopProtectionRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Stop call protection"""

    # Find the call session
    result = await db.execute(
        select(CallSession).where(
            CallSession.call_sid == request.call_sid,
            CallSession.user_id == user_id
        )
    )
    call_session = result.scalar_one_or_none()

    if not call_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call session not found"
        )

    # End the Twilio call
    try:
        twilio_service.end_call(request.call_sid)

        # Update session status
        call_session.status = CallStatus.COMPLETED
        await db.commit()

        logger.info(f"Protection stopped for session {call_session.id}")

        return {"message": "Protection stopped successfully"}

    except Exception as e:
        logger.error(f"Failed to stop protection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop protection: {str(e)}"
        )


@router.get("/status/{call_sid}", response_model=CallStatusResponse)
async def get_call_status(
    call_sid: str,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Get current status of a call"""

    # Find the call session
    result = await db.execute(
        select(CallSession).where(
            CallSession.call_sid == call_sid,
            CallSession.user_id == user_id
        )
    )
    call_session = result.scalar_one_or_none()

    if not call_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call session not found"
        )

    # Get Twilio call status
    twilio_status = twilio_service.get_call_status(call_sid)

    duration = 0.0
    if twilio_status:
        duration = float(twilio_status.get("duration", 0))

    return CallStatusResponse(
        call_sid=call_sid,
        status=call_session.status.value,
        current_risk_score=call_session.max_risk_score,
        duration=duration
    )
