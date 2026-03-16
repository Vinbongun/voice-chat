from __future__ import annotations

import json
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from sqlalchemy import select, insert
from sse_starlette.sse import EventSourceResponse

from app.agent.graph import build_graph
from app.agent.prompts import build_system_prompt
from app.agent.state import AgentState
from app.agent.tools.employees import search_employees
from app.agent.tools.news import search_news
from app.agent.tools.products import search_products
from app.agent.tools.rag import search_documents
from app.agent.tools.tickets import create_ticket, list_tickets
from app.db.database import async_session_maker
from app.db.models import ChatMessage, ChatSession
from app.middleware.auth import get_current_user
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    FeedbackRequest,
    FeedbackResponse,
    UserContext,
)
from app.utils.feedback import save_feedback

router = APIRouter(prefix="/chat", tags=["chat"])

# Build agent once at module load time (startup)
TOOLS = [search_documents, search_employees, search_products, create_ticket, list_tickets, search_news]
agent_graph = build_graph(tools=TOOLS)


def _extract_cards(messages: list) -> list[dict]:
    """Extract structured card data from tool messages."""
    cards = []
    for msg in messages:
        if not isinstance(msg, ToolMessage):
            continue
        try:
            content = msg.content
            data = json.loads(content) if isinstance(content, str) else content
            if isinstance(data, list):
                cards.extend(item for item in data if isinstance(item, dict) and "type" in item)
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    return cards


async def _save_to_db(session_id: str, user_id: str, user_msg: str, result: dict) -> None:
    """Persist user message + assistant response to DB."""
    try:
        async with async_session_maker() as db:
            # Upsert session
            existing = await db.get(ChatSession, uuid.UUID(session_id))
            if not existing:
                db.add(ChatSession(id=uuid.UUID(session_id), user_id=user_id))

            # Save user message
            db.add(ChatMessage(
                session_id=uuid.UUID(session_id),
                role="user",
                content=user_msg,
            ))

            # Save assistant response (cards stored in metadata)
            db.add(ChatMessage(
                id=uuid.UUID(result["message_id"]),
                session_id=uuid.UUID(session_id),
                role="assistant",
                content=result["text"],
                metadata_={"cards": result["cards"]} if result["cards"] else None,
            ))
            await db.commit()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("DB history save failed: %s", e, exc_info=True)


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

    cards = _extract_cards(result["messages"])

    return {
        "session_id": session_id,
        "message_id": str(uuid.uuid4()),
        "text": text,
        "sources": [],
        "cards": cards,
        "actions": [],
    }


@router.post("", response_model=ChatResponse)
@limiter.limit("30/minute")
async def post_chat(
    request: Request,
    body: ChatRequest,
    user: UserContext = Depends(get_current_user),
) -> ChatResponse:
    """Full response endpoint (non-streaming fallback for older clients)."""
    session_id = str(body.session_id) if body.session_id else str(uuid.uuid4())
    try:
        response_data = await _run_agent(body.message, user, session_id)
        await _save_to_db(session_id, user.id, body.message, response_data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ChatResponse(**response_data)


@router.get("/stream")
@limiter.limit("30/minute")
async def stream_chat(
    request: Request,
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
            cards = result["cards"]

            # Persist to DB (best-effort)
            await _save_to_db(session_id, user.id, message, result)

            # Send cards first so UI renders them before text
            if cards:
                yield {"data": json.dumps({"type": "cards", "cards": cards})}

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


@router.post("/feedback", response_model=FeedbackResponse)
async def post_feedback(
    request: FeedbackRequest,
    user: UserContext = Depends(get_current_user),
) -> FeedbackResponse:
    """Save 👍/👎 rating for a chat message."""
    if request.rating not in (1, -1):
        raise HTTPException(status_code=422, detail="Rating must be 1 (👍) or -1 (👎)")

    try:
        async with async_session_maker() as session:
            await save_feedback(
                session=session,
                message_id=request.message_id,
                user_id=user.id,
                rating=request.rating,
                comment=request.comment,
            )
        return FeedbackResponse(success=True, message="Спасибо за оценку!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_chat_history(
    session_id: str = Query(...),
    user: UserContext = Depends(get_current_user),
) -> dict:
    """Load chat history for a session from DB."""
    try:
        async with async_session_maker() as db:
            stmt = (
                select(ChatMessage)
                .where(ChatMessage.session_id == uuid.UUID(session_id))
                .order_by(ChatMessage.created_at)
            )
            result = await db.execute(stmt)
            rows = result.scalars().all()

            messages = []
            for row in rows:
                msg = {
                    "id": str(row.id),
                    "role": row.role,
                    "text": row.content,
                    "cards": row.metadata_.get("cards", []) if row.metadata_ else [],
                    "timestamp": row.created_at.timestamp() * 1000 if row.created_at else None,
                }
                messages.append(msg)

            return {"session_id": session_id, "messages": messages}
    except Exception as e:
        return {"session_id": session_id, "messages": []}
