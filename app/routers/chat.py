from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.middleware.auth import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse, UserContext

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: UserContext = Depends(get_current_user),
) -> ChatResponse:
    """Send a message and receive a complete response.

    TODO: реализовать в Task 6 (LangGraph agent integration).
    """
    raise NotImplementedError("POST /chat not yet implemented — Task 6")


@router.get("/stream")
async def chat_stream(
    message: str,
    session_id: Optional[UUID] = None,
    current_user: UserContext = Depends(get_current_user),
) -> StreamingResponse:
    """Send a message and receive a streaming SSE response.

    TODO: реализовать в Task 6.
    """
    raise NotImplementedError("GET /chat/stream not yet implemented — Task 6")


@router.get("/history")
async def chat_history(
    session_id: UUID,
    limit: int = 50,
    current_user: UserContext = Depends(get_current_user),
) -> list:
    """Get chat history for a session.

    TODO: реализовать в Task 6.
    """
    raise NotImplementedError("GET /chat/history not yet implemented — Task 6")
