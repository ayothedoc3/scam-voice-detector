from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.models.call_session import CallSession
from app.services.twilio.voice import TwilioVoiceService
from app.core.auth import get_current_user

router = APIRouter()


class StartProtectionRequest(BaseModel):
    user_phone: str


class StartProtectionResponse(BaseModel):
    session_id: int
    call_sid: str
    bridge_number: str
    instructions: str


@router.post("/start", response_model=StartProtectionResponse)
async def start_protection(
    request: StartProtectionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start call protection

    Creates a Twilio conference bridge and returns instructions
    for user to merge their suspicious call into the bridge.
    """
    twilio_service = TwilioVoiceService()

    # Create call session in database
    call_session = CallSession(
        user_id=current_user.id,
        call_sid="pending",  # Will be updated by Twilio webhook
        status="initializing"
    )
    db.add(call_session)
    await db.commit()
    await db.refresh(call_session)

    try:
        # Initiate Twilio call
        call_response = await twilio_service.create_protected_call(
            to_number=request.user_phone,
            session_id=call_session.id
        )

        # Update with Twilio call SID
        call_session.call_sid = call_response['call_sid']
        call_session.status = "active"
        await db.commit()

        return StartProtectionResponse(
            session_id=call_session.id,
            call_sid=call_response['call_sid'],
            bridge_number=call_response['bridge_number'],
            instructions="Add this number to your current call using your phone's 'Add Call' feature."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start protection: {str(e)}")
