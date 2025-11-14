from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.call_session import CallSession, CallStatus
from app.models.analysis_result import AnalysisResult
from app.services.twilio_service import twilio_service
from app.services.analysis_service import analysis_service
from app.services.socketio_service import socketio_service
from app.core.config import settings
import logging
from datetime import datetime
import base64

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/voice/{call_session_id}")
async def handle_voice(
    call_session_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Twilio voice webhook - Generate TwiML"""

    logger.info(f"Voice webhook for session {call_session_id}")

    # Generate TwiML for the call
    twiml = twilio_service.generate_initial_twiml(call_session_id)

    return Response(content=twiml, media_type="application/xml")


@router.post("/status/{call_session_id}")
async def handle_status(
    call_session_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle call status updates from Twilio"""

    form_data = await request.form()
    call_status = form_data.get("CallStatus")
    call_sid = form_data.get("CallSid")

    logger.info(f"Status update: {call_status} for session {call_session_id}")

    # Find call session
    result = await db.execute(
        select(CallSession).where(CallSession.id == call_session_id)
    )
    call_session = result.scalar_one_or_none()

    if call_session:
        # Update status based on Twilio callback
        if call_status == "in-progress":
            call_session.status = CallStatus.ACTIVE
        elif call_status in ["completed", "failed", "busy", "no-answer", "canceled"]:
            call_session.status = CallStatus.COMPLETED
            call_session.ended_at = datetime.utcnow()

        await db.commit()

    return {"message": "Status updated"}


@router.post("/conference/{call_session_id}")
async def handle_conference(
    call_session_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle conference status callbacks"""

    form_data = await request.form()
    event = form_data.get("StatusCallbackEvent")
    conference_sid = form_data.get("ConferenceSid")

    logger.info(f"Conference event: {event} for session {call_session_id}")

    # Find call session
    result = await db.execute(
        select(CallSession).where(CallSession.id == call_session_id)
    )
    call_session = result.scalar_one_or_none()

    if call_session and event == "conference-start":
        call_session.conference_sid = conference_sid
        call_session.status = CallStatus.ACTIVE
        await db.commit()

    return {"message": "Conference event handled"}


@router.post("/media/{call_session_id}")
async def handle_media_stream(
    call_session_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Twilio Media Streams - Receive audio data"""

    data = await request.json()
    event = data.get("event")

    if event == "media":
        # Extract audio payload
        media = data.get("media", {})
        payload = media.get("payload")

        if payload:
            # Decode base64 audio
            audio_data = base64.b64decode(payload)

            # Find call session
            result = await db.execute(
                select(CallSession).where(CallSession.id == call_session_id)
            )
            call_session = result.scalar_one_or_none()

            if call_session:
                # Analyze audio chunk
                chunk_index = media.get("chunk", 0)

                analysis_result = await analysis_service.analyze_audio_chunk(
                    audio_data,
                    chunk_index
                )

                # Save analysis result
                db_analysis = AnalysisResult(
                    call_session_id=call_session_id,
                    chunk_index=chunk_index,
                    risk_score=analysis_result["risk_score"],
                    risk_level=analysis_result["risk_level"],
                    is_deepfake=analysis_result["deepfake"]["is_deepfake"],
                    confidence=analysis_result["deepfake"]["confidence"],
                    transcript=analysis_result["transcript"].get("text"),
                    voice_characteristics=analysis_result.get("voice")
                )

                db.add(db_analysis)

                # Update max risk score
                if analysis_result["risk_score"] > call_session.max_risk_score:
                    call_session.max_risk_score = analysis_result["risk_score"]

                await db.commit()

                # Emit real-time update via WebSocket
                await socketio_service.emit_analysis_update(
                    call_session.call_sid,
                    {
                        "timestamp": datetime.utcnow().isoformat(),
                        "chunkIndex": chunk_index,
                        "riskScore": analysis_result["risk_score"],
                        "riskLevel": analysis_result["risk_level"],
                        "deepfake": analysis_result["deepfake"],
                        "transcript": analysis_result["transcript"],
                        "voice": analysis_result.get("voice", {})
                    }
                )

    elif event == "start":
        logger.info(f"Media stream started for session {call_session_id}")

    elif event == "stop":
        logger.info(f"Media stream stopped for session {call_session_id}")

    return {"message": "Media processed"}
