from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Start, Stream, Dial
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TwilioService:
    """Service for Twilio integration"""

    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = settings.TWILIO_PHONE_NUMBER

    def create_protection_call(self, to_number: str, call_session_id: int) -> dict:
        """
        Initiate a call to the user for protection setup

        Args:
            to_number: User's phone number
            call_session_id: Database ID of the call session

        Returns:
            dict with call_sid and other call details
        """
        try:
            # Create TwiML URL for call handling
            twiml_url = f"{settings.BACKEND_URL}/api/v1/twilio/voice/{call_session_id}"

            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                url=twiml_url,
                status_callback=f"{settings.BACKEND_URL}/api/v1/twilio/status/{call_session_id}",
                status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
                status_callback_method='POST',
                record=False  # We'll use Media Streams instead
            )

            logger.info(f"Created call {call.sid} to {to_number}")

            return {
                "call_sid": call.sid,
                "to": to_number,
                "from": self.from_number,
                "status": call.status
            }

        except Exception as e:
            logger.error(f"Failed to create call: {str(e)}")
            raise

    def generate_initial_twiml(self, call_session_id: int) -> str:
        """
        Generate TwiML for the initial call to user
        Instructs user to merge calls
        """
        response = VoiceResponse()

        response.say(
            "Hello from Scam Shield. We're ready to protect your call. "
            "Please tap Add Call, dial the suspicious number, then tap Merge Calls. "
            "We'll analyze the conversation in real-time.",
            voice='alice',
            language='en-US'
        )

        # Create conference and start media streaming
        dial = Dial()
        dial.conference(
            f"scam-shield-{call_session_id}",
            start_conference_on_enter=True,
            end_conference_on_exit=True,
            status_callback=f"{settings.BACKEND_URL}/api/v1/twilio/conference/{call_session_id}",
            status_callback_event=['start', 'end', 'join', 'leave'],
            status_callback_method='POST'
        )
        response.append(dial)

        return str(response)

    def generate_stream_twiml(self, call_session_id: int, stream_url: str) -> str:
        """
        Generate TwiML to start media streaming from the conference

        Args:
            call_session_id: Database ID
            stream_url: WebSocket URL for receiving audio
        """
        response = VoiceResponse()

        # Start media stream
        start = Start()
        stream = Stream(url=stream_url, name=f"stream-{call_session_id}")
        stream.parameter(name="call_session_id", value=str(call_session_id))
        start.append(stream)
        response.append(start)

        # Join conference
        dial = Dial()
        dial.conference(
            f"scam-shield-{call_session_id}",
            start_conference_on_enter=False,
            end_conference_on_exit=False
        )
        response.append(dial)

        return str(response)

    def end_call(self, call_sid: str) -> bool:
        """
        End an active call

        Args:
            call_sid: Twilio call SID

        Returns:
            True if successful
        """
        try:
            call = self.client.calls(call_sid).update(status='completed')
            logger.info(f"Ended call {call_sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to end call {call_sid}: {str(e)}")
            return False

    def get_call_status(self, call_sid: str) -> Optional[dict]:
        """
        Get the current status of a call

        Args:
            call_sid: Twilio call SID

        Returns:
            Call status information
        """
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                "sid": call.sid,
                "status": call.status,
                "duration": call.duration or 0,
                "from": call.from_,
                "to": call.to
            }
        except Exception as e:
            logger.error(f"Failed to get call status for {call_sid}: {str(e)}")
            return None

    def add_participant_to_conference(
        self,
        conference_sid: str,
        participant_number: str,
        call_session_id: int
    ) -> Optional[str]:
        """
        Add a participant to an existing conference

        Args:
            conference_sid: Conference SID
            participant_number: Phone number to add
            call_session_id: Session ID for callbacks

        Returns:
            Call SID of the new participant
        """
        try:
            participant = self.client.conferences(conference_sid).participants.create(
                from_=self.from_number,
                to=participant_number,
                early_media=True,
                end_conference_on_exit=False,
                status_callback=f"{settings.BACKEND_URL}/api/v1/twilio/participant/{call_session_id}",
                status_callback_method='POST'
            )

            logger.info(f"Added participant {participant.call_sid} to conference {conference_sid}")
            return participant.call_sid

        except Exception as e:
            logger.error(f"Failed to add participant: {str(e)}")
            return None

    def end_conference(self, conference_sid: str) -> bool:
        """
        End a conference by removing all participants

        Args:
            conference_sid: Conference SID

        Returns:
            True if successful
        """
        try:
            conference = self.client.conferences(conference_sid).fetch()

            # Remove all participants
            participants = self.client.conferences(conference_sid).participants.list()
            for participant in participants:
                self.client.conferences(conference_sid).participants(participant.call_sid).update(
                    status='completed'
                )

            logger.info(f"Ended conference {conference_sid}")
            return True

        except Exception as e:
            logger.error(f"Failed to end conference {conference_sid}: {str(e)}")
            return False


# Singleton instance
twilio_service = TwilioService()
