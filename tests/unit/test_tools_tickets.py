"""Tests for create_ticket and list_tickets tools — TDD RED phase written first.

Test cases:
1. test_create_ticket_returns_confirmation — mock UIT client, create_ticket returns dict
   with ticket_id, status, message
2. test_create_ticket_includes_user_id — verify UIT client called with correct user_id
   from agent state
3. test_list_tickets_returns_ticket_list — mock UIT client returns tickets, list_tickets
   returns list of dicts
4. test_list_tickets_empty — UIT returns [] → tool returns []
5. test_uit_client_create_calls_correct_endpoint — verify HTTP POST to correct UIT endpoint
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest


# ---------------------------------------------------------------------------
# 1. create_ticket returns confirmation dict with ticket_id, status, message
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_ticket_returns_confirmation(mocker):
    """Tool must return dict with ticket_id, status, and message on success."""
    mocker.patch(
        "app.agent.tools.tickets.uit_client.create_ticket",
        new_callable=AsyncMock,
        return_value={"id": "TK-001", "status": "created", "url": "/tickets/TK-001"},
    )

    from app.agent.tools.tickets import create_ticket

    result = await create_ticket.ainvoke(
        {"user_id": "user-1", "title": "Тест", "description": "Тестовая заявка"}
    )

    assert isinstance(result, dict)
    assert result["ticket_id"] == "TK-001"
    assert result["status"] == "created"
    assert "TK-001" in result["message"]
    assert result["url"] == "/tickets/TK-001"


# ---------------------------------------------------------------------------
# 2. create_ticket passes correct user_id to UIT client
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_ticket_includes_user_id(mocker):
    """Tool must call UIT client with the exact user_id provided as parameter."""
    mock_create = mocker.patch(
        "app.agent.tools.tickets.uit_client.create_ticket",
        new_callable=AsyncMock,
        return_value={"id": "TK-002", "status": "created", "url": "/tickets/TK-002"},
    )

    from app.agent.tools.tickets import create_ticket

    await create_ticket.ainvoke(
        {
            "user_id": "employee-42",
            "title": "Не работает ноутбук",
            "description": "Ноутбук не включается после обновления",
            "category": "IT",
        }
    )

    mock_create.assert_called_once()
    call_kwargs = mock_create.call_args
    # user_id may be passed as positional or keyword arg
    if call_kwargs.args:
        assert call_kwargs.args[0] == "employee-42"
    else:
        assert call_kwargs.kwargs["user_id"] == "employee-42"


# ---------------------------------------------------------------------------
# 3. list_tickets returns list of ticket dicts
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_tickets_returns_ticket_list(mocker):
    """Tool must return list of ticket dicts when UIT client returns tickets."""
    mocker.patch(
        "app.agent.tools.tickets.uit_client.list_tickets",
        new_callable=AsyncMock,
        return_value=[
            {
                "id": "TK-001",
                "title": "Не работает принтер",
                "status": "active",
                "category": "IT",
                "created_at": "2026-03-16",
                "updated_at": "2026-03-16",
            }
        ],
    )

    from app.agent.tools.tickets import list_tickets

    result = await list_tickets.ainvoke({"user_id": "user-1"})

    assert isinstance(result, list)
    assert len(result) == 1
    ticket = result[0]
    assert ticket["id"] == "TK-001"
    assert ticket["title"] == "Не работает принтер"
    assert ticket["status"] == "active"
    assert ticket["category"] == "IT"
    assert ticket["created_at"] == "2026-03-16"
    assert ticket["updated_at"] == "2026-03-16"


# ---------------------------------------------------------------------------
# 4. list_tickets returns empty list when UIT returns []
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_tickets_empty(mocker):
    """Tool must return [] when UIT client returns no tickets."""
    mocker.patch(
        "app.agent.tools.tickets.uit_client.list_tickets",
        new_callable=AsyncMock,
        return_value=[],
    )

    from app.agent.tools.tickets import list_tickets

    result = await list_tickets.ainvoke({"user_id": "user-1"})

    assert result == []


# ---------------------------------------------------------------------------
# 5. UITClient.create_ticket POSTs to correct endpoint with correct payload
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_uit_client_create_calls_correct_endpoint(mocker):
    """UITClient.create_ticket must POST to /tickets with correct user_id in body."""
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "TK-001", "status": "created"}
    mock_response.raise_for_status = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = AsyncMock(return_value=mock_response)

    mocker.patch("app.clients.uit.httpx.AsyncClient", return_value=mock_client)

    from app.clients.uit import UITClient

    client = UITClient()
    result = await client.create_ticket("user-1", "Test", "Test desc")

    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    # First positional arg is the URL
    url_arg = call_args[0][0] if call_args[0] else call_args.args[0]
    assert "/tickets" in url_arg
    assert call_args[1]["json"]["user_id"] == "user-1"
    assert result["id"] == "TK-001"
