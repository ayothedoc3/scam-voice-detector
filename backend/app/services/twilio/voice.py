from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Start, Stream
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class TwilioVoiceService:
    """Handle Twilio Voice operations"""

    def __init__(self):
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self.client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
            self.phone_number = settings.twilio_phone_number
        else:
            logger.warning("Twilio credentials not configured")
            self.client = None
            self.phone_number = None

    async def create_protected_call(self, to_number: str, session_id: int) -> dict:
        """
        Create a call to user for protection

        User will receive call, then add suspicious caller to bridge
        """
        if not self.client:
            raise ValueError("Twilio client not initialized")

        call = self.client.calls.create(
            to=to_number,
            from_=self.phone_number,
            url=f"{settings.app_url}/api/v1/twilio/voice?session_id={session_id}",
            status_callback=f"{settings.app_url}/api/v1/twilio/status",
            status_callback_event=['initiated', 'ringing', 'answered', 'completed']
        )

        return {
            'call_sid': call.sid,
            'bridge_number': self.phone_number
        }

    def generate_protection_twiml(self, call_sid: str) -> VoiceResponse:
        """
        Generate TwiML for protected call

        Starts Media Streams to receive audio
        """
        response = VoiceResponse()

        response.say(
            "Scam Shield activated. Add your suspicious caller now.",
            voice='Polly.Joanna'
        )

        # Start Media Streams
        start = Start()
        stream = Stream(
            url=f"wss://{settings.app_domain}/api/v1/twilio/media-stream",
            track='inbound_track'
        )
        start.append(stream)
        response.append(start)

        # Keep call open for 5 minutes
        response.pause(length=300)

        return response
