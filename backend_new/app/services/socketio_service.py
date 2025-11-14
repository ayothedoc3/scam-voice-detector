import socketio
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)


class SocketIOService:
    """Service for Socket.IO real-time communication"""

    def __init__(self):
        self.sio = sio

    async def emit_analysis_update(self, call_sid: str, analysis_data: dict):
        """
        Emit real-time analysis update to connected clients

        Args:
            call_sid: Call SID to identify the room
            analysis_data: Analysis result data
        """
        try:
            room = f"call_{call_sid}"

            # Emit to all clients in the room
            await self.sio.emit(
                'analysis_update',
                analysis_data,
                room=room
            )

            logger.info(f"Emitted analysis update to room {room}")

        except Exception as e:
            logger.error(f"Failed to emit analysis update: {str(e)}")

    async def emit_real_time_analysis(self, call_sid: str, data: dict):
        """
        Emit real-time analysis event

        Args:
            call_sid: Call session ID
            data: Analysis data
        """
        try:
            room = f"call_{call_sid}"
            await self.sio.emit('real_time_analysis', data, room=room)
            logger.info(f"Emitted real-time analysis to {room}")
        except Exception as e:
            logger.error(f"Failed to emit real-time analysis: {str(e)}")

    async def join_call_room(self, sid: str, call_sid: str):
        """
        Add client to a call-specific room

        Args:
            sid: Socket session ID
            call_sid: Call SID
        """
        room = f"call_{call_sid}"
        await self.sio.enter_room(sid, room)
        logger.info(f"Client {sid} joined room {room}")

    async def leave_call_room(self, sid: str, call_sid: str):
        """
        Remove client from a call-specific room

        Args:
            sid: Socket session ID
            call_sid: Call SID
        """
        room = f"call_{call_sid}"
        await self.sio.leave_room(sid, room)
        logger.info(f"Client {sid} left room {room}")


# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    logger.info(f"Client connected: {sid}")
    await sio.emit('connected', {'status': 'connected'}, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")


@sio.event
async def join_call(sid, data):
    """Handle client joining a call room"""
    call_sid = data.get('call_sid')
    if call_sid:
        room = f"call_{call_sid}"
        await sio.enter_room(sid, room)
        logger.info(f"Client {sid} joined call room {room}")
        await sio.emit('joined', {'call_sid': call_sid}, room=sid)


@sio.event
async def leave_call(sid, data):
    """Handle client leaving a call room"""
    call_sid = data.get('call_sid')
    if call_sid:
        room = f"call_{call_sid}"
        await sio.leave_room(sid, room)
        logger.info(f"Client {sid} left call room {room}")


# Singleton instance
socketio_service = SocketIOService()
