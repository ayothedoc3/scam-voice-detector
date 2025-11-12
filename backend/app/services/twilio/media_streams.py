import asyncio
import base64
import audioop
import io
import wave
from datetime import datetime
import logging
from contextlib import asynccontextmanager

from app.db.session import AsyncSessionLocal
from app.models.call_session import CallSession
from app.models.analysis_result import AnalysisResult

logger = logging.getLogger(__name__)


class MediaStreamHandler:
    """Handles Twilio Media Streams"""

    def __init__(self):
        self.active_sessions = {}
        self.sample_rate = 8000
        self.chunk_duration_seconds = 10
        self.chunk_size_bytes = self.sample_rate * self.chunk_duration_seconds * 2

    async def handle_stream_start(self, data: dict, call_sid: str):
        """Handle start of media stream"""
        stream_sid = data.get('streamSid')

        logger.info(f"Media stream started: {stream_sid} for call {call_sid}")

        session = CallStreamSession(
            stream_sid=stream_sid,
            call_sid=call_sid,
            sample_rate=self.sample_rate,
            chunk_duration=self.chunk_duration_seconds
        )

        self.active_sessions[stream_sid] = session

        # Update database
        try:
            async with AsyncSessionLocal() as db:
                from sqlalchemy import select
                result = await db.execute(
                    select(CallSession).where(CallSession.call_sid == call_sid)
                )
                call_session = result.scalar_one_or_none()
                if call_session:
                    call_session.stream_sid = stream_sid
                    await db.commit()
                    session.db_id = call_session.id
        except Exception as e:
            logger.error(f"Error updating call session: {str(e)}")

    async def handle_media(self, data: dict):
        """Handle incoming media payload"""
        stream_sid = data.get('streamSid')

        if stream_sid not in self.active_sessions:
            return

        session = self.active_sessions[stream_sid]

        # Extract audio
        payload_base64 = data.get('media', {}).get('payload')
        if not payload_base64:
            return

        try:
            # Decode μ-law to PCM
            audio_bytes = base64.b64decode(payload_base64)
            pcm_audio = audioop.ulaw2lin(audio_bytes, 2)

            session.add_audio_chunk(pcm_audio)

            if session.should_analyze():
                await self.analyze_chunk(session)

        except Exception as e:
            logger.error(f"Error processing media: {str(e)}")

    async def analyze_chunk(self, session):
        """Analyze audio chunk"""
        logger.info(f"Analyzing chunk {session.chunk_count} for stream {session.stream_sid}")

        audio_data = session.get_buffer_as_wav()

        try:
            # Import here to avoid circular dependencies
            from app.services.detection.deepfake_detector import DeepfakeDetector
            from app.services.audio.analyzer import VoiceAnalyzer

            deepfake_detector = DeepfakeDetector()
            voice_analyzer = VoiceAnalyzer()

            # Run parallel analysis
            deepfake_result, voice_result = await asyncio.gather(
                deepfake_detector.analyze(audio_data),
                voice_analyzer.analyze(audio_data),
                return_exceptions=True
            )

            # Calculate risk score
            risk_score = self.calculate_risk_score(deepfake_result, voice_result)
            risk_level = self.get_risk_level(risk_score)

            analysis_result = {
                'timestamp': datetime.utcnow().isoformat(),
                'chunk_index': session.chunk_count,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'deepfake': deepfake_result if not isinstance(deepfake_result, Exception) else None,
                'voice': voice_result if not isinstance(voice_result, Exception) else None
            }

            # Store in database
            await self.store_analysis(session, analysis_result)

            # Push to frontend via WebSocket
            try:
                from app.websocket.server import sio
                await sio.emit(
                    'analysis_update',
                    analysis_result,
                    room=session.call_sid
                )

                # Send alert if high risk
                if risk_score >= 70:
                    await sio.emit(
                        'high_risk_alert',
                        {
                            'risk_score': risk_score,
                            'risk_level': risk_level,
                            'message': f'⚠️ SCAM DETECTED - {risk_score:.0f}% confidence'
                        },
                        room=session.call_sid
                    )
            except Exception as e:
                logger.error(f"Error emitting websocket event: {str(e)}")

            session.clear_buffer()

        except Exception as e:
            logger.error(f"Analysis error: {str(e)}", exc_info=True)

    async def handle_stream_stop(self, data: dict):
        """Handle end of media stream"""
        stream_sid = data.get('streamSid')

        if stream_sid in self.active_sessions:
            session = self.active_sessions[stream_sid]

            # Process remaining audio
            if session.has_audio():
                await self.analyze_chunk(session)

            # Update database
            try:
                async with AsyncSessionLocal() as db:
                    if session.db_id:
                        call_session = await db.get(CallSession, session.db_id)
                        if call_session:
                            call_session.status = 'completed'
                            call_session.ended_at = datetime.utcnow()
                            await db.commit()
            except Exception as e:
                logger.error(f"Error updating call session on stop: {str(e)}")

            del self.active_sessions[stream_sid]

    def calculate_risk_score(self, deepfake_result, voice_result) -> float:
        """Calculate aggregate risk score"""
        scores = []
        weights = []

        if deepfake_result and not isinstance(deepfake_result, Exception):
            scores.append(deepfake_result.get('confidence', 0) * 100)
            weights.append(0.7)

        if voice_result and not isinstance(voice_result, Exception):
            scores.append(voice_result.get('synthetic_score', 0))
            weights.append(0.3)

        if not scores:
            return 0.0

        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        return min(weighted_sum / sum(weights), 100.0)

    def get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to level"""
        if risk_score >= 86:
            return 'CRITICAL'
        elif risk_score >= 61:
            return 'HIGH'
        elif risk_score >= 31:
            return 'MEDIUM'
        else:
            return 'LOW'

    async def store_analysis(self, session, result):
        """Store analysis in database"""
        try:
            async with AsyncSessionLocal() as db:
                if session.db_id:
                    analysis = AnalysisResult(
                        call_session_id=session.db_id,
                        chunk_index=session.chunk_count,
                        risk_score=result['risk_score'],
                        risk_level=result['risk_level'],
                        deepfake_data=result.get('deepfake'),
                        voice_data=result.get('voice')
                    )
                    db.add(analysis)
                    await db.commit()
        except Exception as e:
            logger.error(f"Error storing analysis: {str(e)}")


class CallStreamSession:
    """Manages audio buffering for a call stream"""

    def __init__(self, stream_sid, call_sid, sample_rate, chunk_duration):
        self.stream_sid = stream_sid
        self.call_sid = call_sid
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.chunk_size_bytes = sample_rate * chunk_duration * 2

        self.audio_buffer = bytearray()
        self.chunk_count = 0
        self.total_duration = 0.0
        self.db_id = None

    def add_audio_chunk(self, audio_bytes):
        """Add audio to buffer"""
        self.audio_buffer.extend(audio_bytes)
        self.total_duration += len(audio_bytes) / (self.sample_rate * 2)

    def should_analyze(self):
        """Check if ready to analyze"""
        return len(self.audio_buffer) >= self.chunk_size_bytes

    def has_audio(self):
        """Check if buffer has audio"""
        return len(self.audio_buffer) > 0

    def get_buffer_as_wav(self):
        """Convert buffer to WAV"""
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(bytes(self.audio_buffer[:self.chunk_size_bytes]))
        return wav_buffer.getvalue()

    def clear_buffer(self):
        """Clear analyzed audio"""
        self.audio_buffer = self.audio_buffer[self.chunk_size_bytes:]
        self.chunk_count += 1
