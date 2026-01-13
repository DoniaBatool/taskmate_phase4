"""ChatKit Protocol Adapter for Custom Backend.

This endpoint adapts ChatKit protocol requests to our existing chat endpoint format.
ChatKit sends requests in its own protocol, but our backend uses a simpler REST format.
This adapter converts between the two.
"""

import json
import logging
from typing import Any, Dict
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from sqlmodel import Session

from ..auth.dependencies import get_current_user
from ..db import get_session
from .chat import chat, ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chatkit"])


@router.post("/chatkit")
async def chatkit_adapter(
    request: Request,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Adapter endpoint that converts ChatKit protocol to our chat endpoint format.
    
    ChatKit sends requests in its own protocol format. This endpoint:
    1. Receives ChatKit protocol requests
    2. Extracts user message and thread/conversation info
    3. Converts to our ChatRequest format
    4. Calls our existing chat endpoint logic
    5. Converts response back to ChatKit format
    
    Args:
        request: FastAPI request object
        current_user_id: Authenticated user ID from JWT
        db: Database session
        
    Returns:
        ChatKit-compatible response (streaming or JSON)
    """
    try:
        # Read request body
        body = await request.body()
        
        # Try to parse as JSON
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            # If not JSON, might be ChatKit protocol format
            payload = {"raw": body.decode('utf-8')}
        
        logger.info(
            f"ChatKit request received for user {current_user_id}",
            extra={"payload_keys": list(payload.keys()) if isinstance(payload, dict) else []}
        )
        
        # Extract message from ChatKit payload
        # ChatKit sends requests in SSE format or JSON with messages array
        message_text = None
        conversation_id = None
        thread_id = None
        
        if isinstance(payload, dict):
            # ChatKit typically sends messages array with role and content
            if "messages" in payload and isinstance(payload["messages"], list):
                # ChatKit messages array format - get the last user message
                for msg in reversed(payload["messages"]):
                    if isinstance(msg, dict) and msg.get("role") == "user":
                        # Content can be string or array of content items
                        content = msg.get("content")
                        if isinstance(content, str):
                            message_text = content
                        elif isinstance(content, list) and len(content) > 0:
                            # Get text from first content item
                            first_item = content[0]
                            if isinstance(first_item, dict):
                                message_text = first_item.get("text") or first_item.get("content")
                            elif isinstance(first_item, str):
                                message_text = first_item
                        break
            
            # Also check for direct text/message fields
            if not message_text:
                if "text" in payload:
                    message_text = payload["text"]
                elif "message" in payload:
                    message_text = payload["message"]
                elif "content" in payload:
                    message_text = payload["content"]
            
            # Extract thread/conversation ID if present
            if "thread_id" in payload:
                thread_id = payload["thread_id"]
                try:
                    conversation_id = int(thread_id) if thread_id else None
                except (ValueError, TypeError):
                    pass
            elif "conversation_id" in payload:
                try:
                    conversation_id = int(payload["conversation_id"])
                except (ValueError, TypeError):
                    pass
        
        # If no message found, return error
        if not message_text:
            logger.warning(
                f"Could not extract message from ChatKit payload",
                extra={"payload": str(payload)[:200]}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message not found in request"
            )
        
        # Create ChatRequest in our format
        chat_request = ChatRequest(
            message=message_text,
            conversation_id=conversation_id
        )
        
        # Call our existing chat endpoint logic
        # We need to call it directly since it's an async function
        chat_response = await chat(
            user_id=current_user_id,
            request=chat_request,
            current_user_id=current_user_id,
            db=db
        )
        
        # Convert our ChatResponse to ChatKit format
        # ChatKit expects SSE (Server-Sent Events) format with specific event structure
        # Format: event: <event_type>\ndata: <json_data>\n\n
        
        async def generate_sse_stream():
            """Generate SSE stream for ChatKit response."""
            import uuid
            
            response_thread_id = str(chat_response.conversation_id)
            
            # Send thread metadata event if new conversation
            if conversation_id is None:
                yield f"event: thread.created\n"
                yield f"data: {json.dumps({'id': response_thread_id, 'metadata': {}})}\n\n"
            
            # Generate unique message ID
            message_id = f"msg_{uuid.uuid4().hex[:12]}"
            
            # Message item created event (ChatKit expects this format)
            yield f"event: thread.message.item.created\n"
            message_data = {
                "id": message_id,
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": chat_response.response
                    }
                ],
                "content_type": "output_text"
            }
            yield f"data: {json.dumps(message_data)}\n\n"
            
            # Add tool calls as annotations if any
            if chat_response.tool_calls:
                for tool_call in chat_response.tool_calls:
                    tool_name = tool_call.get("tool", "unknown")
                    tool_params = tool_call.get("params", {})
                    tool_result = tool_call.get("result", {})
                    
                    # Send tool call annotation
                    yield f"event: thread.message.item.annotation.created\n"
                    annotation_data = {
                        "id": f"annotation_{uuid.uuid4().hex[:12]}",
                        "message_id": message_id,
                        "type": "tool_call",
                        "tool_name": tool_name,
                        "tool_params": tool_params,
                        "tool_result": tool_result
                    }
                    yield f"data: {json.dumps(annotation_data)}\n\n"
            
            # Send thread message completed event
            yield f"event: thread.message.completed\n"
            yield f"data: {json.dumps({'id': message_id, 'thread_id': response_thread_id})}\n\n"
        
        logger.info(
            f"ChatKit SSE response prepared for user {current_user_id}",
            extra={"conversation_id": chat_response.conversation_id}
        )
        
        return StreamingResponse(
            generate_sse_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"ChatKit adapter error: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process ChatKit request: {str(e)}"
        )
