from __future__ import annotations

import json
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from langchain_core.messages import HumanMessage, SystemMessage
from sse_starlette.sse import EventSourceResponse

from app.agent.graph import build_graph
from app.agent.prompts import build_system_prompt
from app.agent.state import AgentState
from app.agent.tools.employees import search_employees
from app.agent.tools.rag import search_documents
from app.middleware.auth import get_current_user
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    UserContext,
)

router = APIRouter(prefix="/chat", tags=["chat"])

# Build agent once at module load time (startup)
TOOLS = [search_documents, search_employees]
agent_graph = build_graph(tools=TOOLS)


async def _run_agent(message: str, user: UserContext, session_id: str) -> dict:
    """Run the LangGraph agent and return a response dict."""
    system_prompt = build_system_prompt(user)

    state = AgentState(
        messages=[
            SystemMessage(content=system_prompt),
            HumanMessage(content=message),
        ],
        user=user,
        session_id=session_id,
    )

    result = await agent_graph.ainvoke(state)

    # Extract the last AI message content
    final_message = result["messages"][-1]
    text = (
        final_message.content
        if hasattr(final_message, "content")
        else str(final_message)
    )

    return {
        "session_id": session_id,
        "message_id": str(uuid.uuid4()),
        "text": text,
        "sources": [],
        "cards": [],
        "actions": [],
    }


@router.post("", response_model=ChatResponse)
async def post_chat(
    request: ChatRequest,
    user: UserContext = Depends(get_current_user),
) -> ChatResponse:
    """Full response endpoint (non-streaming fallback for older clients)."""
    session_id = str(request.session_id) if request.session_id else str(uuid.uuid4())
    try:
        response_data = await _run_agent(request.message, user, session_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ChatResponse(**response_data)


@router.get("/stream")
async def stream_chat(
    message: str = Query(...),
    session_id: Optional[str] = Query(None),
    user: UserContext = Depends(get_current_user),
) -> EventSourceResponse:
    """SSE streaming endpoint — sends text deltas then a done event."""
    if not session_id:
        session_id = str(uuid.uuid4())

    async def event_generator():
        try:
            result = await _run_agent(message, user, session_id)
            text = result["text"]

            # Stream text word-by-word
            words = text.split()
            for i, word in enumerate(words):
                chunk = word + (" " if i < len(words) - 1 else "")
                yield {"data": json.dumps({"type": "text_delta", "delta": chunk})}

            # Signal completion
            yield {
                "data": json.dumps(
                    {
                        "type": "done",
                        "session_id": session_id,
                        "message_id": result["message_id"],
                    }
                )
            }

        except Exception as exc:
            yield {"data": json.dumps({"type": "error", "message": str(exc)})}

    return EventSourceResponse(event_generator())


@router.get("/history")
async def get_chat_history(
    session_id: str = Query(...),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Get chat history for a session.

    TODO (Task 7): integrate with PostgresChatMessageHistory.
    """
    # Stub — returns empty messages list until Task 7 integrates DB history
    return {"session_id": session_id, "messages": []}
