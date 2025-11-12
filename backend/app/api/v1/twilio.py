from fastapi import APIRouter, Request, Response
from app.services.twilio.media_streams import MediaStreamHandler
from app.services.twilio.voice import TwilioVoiceService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize handler
media_stream_handler = MediaStreamHandler()


@router.post("/voice")
async def voice_webhook(request: Request):
    """
    Twilio voice webhook

    Called when user connects to Twilio number
    """
    form_data = await request.form()
    call_sid = form_data.get('CallSid')
    session_id = request.query_params.get('session_id')

    logger.info(f"Voice webhook for call: {call_sid}, session: {session_id}")

    twilio_service = TwilioVoiceService()
    twiml = twilio_service.generate_protection_twiml(call_sid)

    return Response(content=str(twiml), media_type="application/xml")


@router.post("/media-stream")
async def media_stream_webhook(request: Request):
    """
    Twilio Media Streams webhook

    Receives real-time audio stream from Twilio
    """
    try:
        data = await request.json()
        event = data.get('event')

        if event == 'start':
            call_sid = data.get('start', {}).get('callSid')
            await media_stream_handler.handle_stream_start(data, call_sid)
        elif event == 'media':
            await media_stream_handler.handle_media(data)
        elif event == 'stop':
            await media_stream_handler.handle_stream_stop(data)

        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Media stream error: {str(e)}", exc_info=True)
        return {"status": "error", "message": str(e)}


@router.post("/status")
async def status_webhook(request: Request):
    """
    Twilio status callback webhook

    Receives call status updates
    """
    form_data = await request.form()
    call_sid = form_data.get('CallSid')
    call_status = form_data.get('CallStatus')

    logger.info(f"Call {call_sid} status: {call_status}")

    return {"status": "ok"}
