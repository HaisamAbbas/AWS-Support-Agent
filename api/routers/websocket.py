"""
WebSocket Router for Streaming Responses
Handles real-time streaming of agent responses using Socket.IO.
"""
import socketio
from fastapi import APIRouter
import asyncio
from api.agent_service import agent_service

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=False
)

# Create Socket.IO ASGI app
socket_app = socketio.ASGIApp(sio)

router = APIRouter()


@sio.event
async def connect(sid, environ, auth):
    """Handle client connection."""
    print(f"Client connected: {sid}")
    
    # Validate auth token (API key)
    token = auth.get('token') if auth else None
    if not token or len(token) < 5:
        await sio.emit('error', {'message': 'Invalid authentication token'}, room=sid)
        await sio.disconnect(sid)
        return False
    
    # Store token in session
    await sio.save_session(sid, {'token': token, 'authenticated': True})
    print(f"Client {sid} authenticated")
    return True


@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    print(f"Client disconnected: {sid}")


@sio.event
async def query(sid, data):
    """
    Handle streaming query from client.
    
    Expected data format:
    {
        "query": "What is AWS EC2?",
        "include_sources": false
    }
    """
    try:
        # Verify authentication
        session = await sio.get_session(sid)
        if not session.get('authenticated'):
            await sio.emit('error', {'message': 'Not authenticated'}, room=sid)
            return
        
        # Get query parameters
        query_text = data.get('query', '').strip()
        include_sources = data.get('include_sources', False)
        
        if not query_text:
            await sio.emit('error', {'message': 'Query is required'}, room=sid)
            return
        
        # Check if agent is initialized
        if not agent_service.get_status()["initialized"]:
            await sio.emit('error', {'message': 'Agent not initialized'}, room=sid)
            return
        
        # Stream the response
        # For now, we'll simulate streaming by chunking the response
        # In production, integrate with LLM streaming API
        result = agent_service.query_agent(query_text, include_sources)
        
        response_text = result.get('response', '')
        
        # Simulate streaming by sending chunks
        chunk_size = 10  # words per chunk
        words = response_text.split()
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size]) + ' '
            await sio.emit('chunk', {'chunk': chunk}, room=sid)
            await asyncio.sleep(0.1)  # Small delay for streaming effect
        
        # Send completion event
        await sio.emit('complete', {
            'query': query_text,
            'processing_time': result.get('processing_time'),
            'timestamp': result.get('timestamp'),
            'sources': result.get('sources')
        }, room=sid)
        
    except Exception as e:
        print(f"Error in query handler: {e}")
        await sio.emit('error', {'message': str(e)}, room=sid)


# Mount the Socket.IO app
def get_socket_app():
    """Return the Socket.IO ASGI app for mounting."""
    return socket_app
