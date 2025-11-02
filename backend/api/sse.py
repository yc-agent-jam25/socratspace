"""
Server-Side Events (SSE) manager for real-time updates to frontend
Replaces WebSocket with simpler SSE implementation
"""

from fastapi import Request
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional
import json
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SSEManager:
    """
    Manages SSE connections and broadcasts events
    
    For each session, maintains a queue of events to send
    """

    def __init__(self):
        # session_id -> list of event queues (one per connected client)
        self.session_queues: Dict[str, list] = {}

    async def subscribe(self, session_id: str) -> asyncio.Queue:
        """
        Subscribe to events for a session
        
        Returns a queue that will receive events
        """
        if session_id not in self.session_queues:
            self.session_queues[session_id] = []
        
        queue = asyncio.Queue()
        self.session_queues[session_id].append(queue)
        
        logger.info(f"SSE subscribed for session {session_id}. Total clients: {len(self.session_queues[session_id])}")
        return queue

    async def unsubscribe(self, session_id: str, queue: asyncio.Queue):
        """
        Unsubscribe from events for a session
        """
        if session_id in self.session_queues:
            try:
                self.session_queues[session_id].remove(queue)
                logger.info(f"SSE unsubscribed for session {session_id}. Remaining clients: {len(self.session_queues[session_id])}")
                
                # Clean up empty session
                if not self.session_queues[session_id]:
                    del self.session_queues[session_id]
                    logger.info(f"Session {session_id} has no more clients. Removed.")
            except ValueError:
                pass

    async def broadcast(self, session_id: str, event_type: str, data: Dict[str, Any]):
        """
        Broadcast event to all clients subscribed to a session
        
        Args:
            session_id: Session ID to broadcast to
            event_type: Type of event (phase_change, agent_message, etc.)
            data: Event data
        """
        if session_id not in self.session_queues:
            logger.warning(f"No SSE clients for session {session_id}")
            return

        message = {
            "type": event_type,
            "data": data
        }

        # Send to all queues for this session
        for queue in self.session_queues[session_id]:
            try:
                await queue.put(message)
            except Exception as e:
                logger.error(f"Error broadcasting to queue: {e}")

    async def send_phase_change(self, session_id: str, phase: str):
        """Broadcast phase change"""
        await self.broadcast(session_id, "phase_change", {
            "phase": phase,
            "timestamp": datetime.now().isoformat()
        })

    async def send_agent_message(
        self,
        session_id: str,
        agent: str,
        message: str,
        message_type: str = "info"
    ):
        """Broadcast agent message"""
        await self.broadcast(session_id, "agent_message", {
            "agent": agent,
            "message": message,
            "message_type": message_type,
            "timestamp": int(datetime.now().timestamp() * 1000)
        })

    async def send_decision(self, session_id: str, decision: Dict[str, Any]):
        """Broadcast final decision"""
        await self.broadcast(session_id, "decision", decision)

    async def send_error(self, session_id: str, error_message: str, error_code: str = "ERROR"):
        """Broadcast error"""
        await self.broadcast(session_id, "error", {
            "message": error_message,
            "code": error_code,
            "timestamp": datetime.now().isoformat()
        })
    
    async def send_oauth_request(self, session_id: str, mcp_name: str, auth_url: str, oauth_session_id: str):
        """Broadcast OAuth authentication request to frontend"""
        await self.broadcast(session_id, "oauth_request", {
            "mcp_name": mcp_name,
            "auth_url": auth_url,
            "oauth_session_id": oauth_session_id,
            "timestamp": datetime.now().isoformat()
        })

    async def send_ping(self, session_id: str):
        """Send heartbeat ping"""
        await self.broadcast(session_id, "ping", {})

    def stream_events(self, session_id: str, request: Request):
        """
        Create an SSE stream for a session
        
        This is the generator function that yields SSE events
        """
        async def event_generator():
            queue = await self.subscribe(session_id)
            
            try:
                # Send initial connection message
                yield f"data: {json.dumps({'type': 'connected', 'data': {'session_id': session_id}})}\n\n"
                
                # Send periodic pings to keep connection alive
                ping_interval = 30  # seconds
                last_ping = datetime.now()
                
                while True:
                    # Check if client disconnected
                    if await request.is_disconnected():
                        logger.info(f"SSE client disconnected for session {session_id}")
                        break

                    # Send ping if needed
                    now = datetime.now()
                    if (now - last_ping).total_seconds() >= ping_interval:
                        yield f"data: {json.dumps({'type': 'ping', 'data': {}})}\n\n"
                        last_ping = now

                    # Try to get message from queue (with timeout)
                    try:
                        message = await asyncio.wait_for(queue.get(), timeout=1.0)
                        yield f"data: {json.dumps(message)}\n\n"
                    except asyncio.TimeoutError:
                        # No message, continue loop to check connection and send ping
                        continue

            except asyncio.CancelledError:
                logger.info(f"SSE stream cancelled for session {session_id}")
            except Exception as e:
                logger.error(f"SSE stream error for session {session_id}: {e}")
                yield f"data: {json.dumps({'type': 'error', 'data': {'message': str(e)}})}\n\n"
            finally:
                # Cleanup
                await self.unsubscribe(session_id, queue)

        return event_generator()


# Global SSE manager instance
sse_manager = SSEManager()

