"""Integration tests for chat endpoints: POST /chat, GET /chat/stream, GET /chat/history.

TDD: these tests are written FIRST (RED phase) before implementation.
"""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock

from langchain_core.messages import AIMessage


@pytest.mark.asyncio
async def test_post_chat_returns_200_with_response(auth_client, mocker):
    """POST /chat with message returns 200 with session_id, message_id, text."""
    mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content="Ответ агента")]},
    )
    response = await auth_client.post("/chat", json={"message": "Привет"})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "message_id" in data
    assert "text" in data
    assert data["text"] == "Ответ агента"


@pytest.mark.asyncio
async def test_post_chat_requires_auth(client):
    """POST /chat without auth returns 401."""
    response = await client.post("/chat", json={"message": "Привет"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_post_chat_with_session_id(auth_client, mocker):
    """POST /chat with explicit session_id preserves it in response."""
    mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content="Ответ с сессией")]},
    )
    session_id = "12345678-1234-5678-1234-567812345678"
    response = await auth_client.post(
        "/chat", json={"message": "Привет", "session_id": session_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["text"] == "Ответ с сессией"


@pytest.mark.asyncio
async def test_post_chat_response_has_required_fields(auth_client, mocker):
    """POST /chat response contains all required ChatResponse fields."""
    mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content="Полный ответ")]},
    )
    response = await auth_client.post("/chat", json={"message": "Тест"})
    assert response.status_code == 200
    data = response.json()
    # Required fields from ChatResponse schema
    assert "session_id" in data
    assert "message_id" in data
    assert "text" in data
    assert "sources" in data
    assert "cards" in data
    assert "actions" in data
    assert isinstance(data["sources"], list)
    assert isinstance(data["cards"], list)
    assert isinstance(data["actions"], list)


@pytest.mark.asyncio
async def test_get_chat_history_returns_messages(auth_client, mocker):
    """GET /chat/history?session_id=... returns session_id and messages list."""
    session_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    response = await auth_client.get(f"/chat/history?session_id={session_id}")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["session_id"] == session_id
    assert "messages" in data
    assert isinstance(data["messages"], list)


@pytest.mark.asyncio
async def test_get_chat_history_requires_auth(client):
    """GET /chat/history without auth returns 401."""
    response = await client.get("/chat/history?session_id=some-session")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_stream_endpoint_exists(auth_client, mocker):
    """GET /chat/stream returns 200 with SSE content-type header."""
    mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content="Ответ")]},
    )
    response = await auth_client.get("/chat/stream?message=Привет")
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_stream_endpoint_requires_auth(client):
    """GET /chat/stream without auth returns 401."""
    response = await client.get("/chat/stream?message=Привет")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_stream_endpoint_requires_message_param(auth_client, mocker):
    """GET /chat/stream without message query param returns 422."""
    response = await auth_client.get("/chat/stream")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_chat_history_requires_session_id(auth_client):
    """History endpoint requires session_id query param."""
    response = await auth_client.get("/chat/history")
    assert response.status_code == 422
