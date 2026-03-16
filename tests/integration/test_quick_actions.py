"""Tests for quick action endpoint."""
import pytest
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_quick_action_my_vacation(auth_client):
    response = await auth_client.post("/chat/quick-action", json={"action": "my_vacation"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "отпуск" in data["message"].lower() or "vacation" in data["message"].lower()


@pytest.mark.asyncio
async def test_quick_action_unknown_returns_400(auth_client):
    response = await auth_client.post("/chat/quick-action", json={"action": "unknown_action"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_quick_action_requires_auth(client):
    response = await client.post("/chat/quick-action", json={"action": "my_vacation"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_quick_action_my_tickets(auth_client):
    response = await auth_client.post("/chat/quick-action", json={"action": "my_tickets"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_quick_action_all_valid_actions(auth_client):
    """All 5 defined actions return 200."""
    actions = ["my_vacation", "my_tickets", "find_employee", "find_product", "it_help"]
    for action in actions:
        response = await auth_client.post("/chat/quick-action", json={"action": action})
        assert response.status_code == 200, f"Action {action} failed"
