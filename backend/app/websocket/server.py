import socketio
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.cors_origins_list,
    logger=True,
    engineio_logger=True
)

sio_app = socketio.ASGIApp(sio, socketio_path='/socket.io')


@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    logger.info(f"Client connected: {sid}")
    await sio.emit('connected', {'message': 'Connected to Scam Shield'}, to=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")


@sio.event
async def join_call(sid, data):
    """Join call room for real-time updates"""
    call_sid = data.get('call_sid')
    if call_sid:
        await sio.enter_room(sid, call_sid)
        logger.info(f"Client {sid} joined call room: {call_sid}")
        await sio.emit('joined_call', {'call_sid': call_sid}, to=sid)


@sio.event
async def leave_call(sid, data):
    """Leave call room"""
    call_sid = data.get('call_sid')
    if call_sid:
        await sio.leave_room(sid, call_sid)
        logger.info(f"Client {sid} left call room: {call_sid}")
