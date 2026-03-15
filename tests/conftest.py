import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def auth_client():
    """Client with mocked auth returning test user."""
    from app.middleware.auth import get_current_user
    from app.schemas.chat import UserContext

    app.dependency_overrides[get_current_user] = lambda: UserContext(
        id="test-user-id", name="Test User", position="Developer",
        department="IT", city="Moscow"
    )
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
