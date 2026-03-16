"""Tests for feedback functionality."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.utils.feedback import save_feedback


@pytest.mark.asyncio
async def test_save_feedback_thumbs_up():
    """save_feedback with rating=1 creates MessageFeedback."""
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await save_feedback(mock_session, uuid4(), "user-1", 1)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_feedback_thumbs_down():
    """save_feedback with rating=-1 works correctly."""
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await save_feedback(mock_session, uuid4(), "user-1", -1)
    mock_session.add.assert_called_once()


@pytest.mark.asyncio
async def test_save_feedback_invalid_rating():
    """Invalid rating raises ValueError."""
    mock_session = AsyncMock()
    with pytest.raises(ValueError, match="Rating must be 1 or -1"):
        await save_feedback(mock_session, uuid4(), "user-1", 0)


@pytest.mark.asyncio
async def test_feedback_endpoint_returns_200(auth_client, mocker):
    """POST /chat/feedback with valid data returns 200."""
    mocker.patch("app.routers.chat.save_feedback", new_callable=AsyncMock)
    mocker.patch("app.routers.chat.async_session_maker")

    msg_id = str(uuid4())
    response = await auth_client.post("/chat/feedback", json={
        "message_id": msg_id,
        "rating": 1,
    })
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_feedback_endpoint_requires_auth(client):
    """Feedback endpoint requires authentication."""
    response = await client.post("/chat/feedback", json={
        "message_id": str(uuid4()),
        "rating": 1,
    })
    assert response.status_code == 401
