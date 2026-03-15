from __future__ import annotations

from typing import Any

import httpx

from app.config import settings


class Bitrix24Client:
    """Bitrix24 REST API client for CRM, tasks, news, and employee photo URLs."""

    def __init__(self) -> None:
        self.webhook_url = settings.BITRIX24_WEBHOOK_URL
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Bitrix24Client:
        self._client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def get_user_photo(self, bitrix_id: str) -> str | None:
        """Get employee photo URL by Bitrix24 user ID."""
        if not self.webhook_url or not bitrix_id:
            return None
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.webhook_url}/user.get",
                params={"ID": bitrix_id},
                timeout=10.0,
            )
            if response.status_code != 200:
                return None
            data = response.json()
            users = data.get("result", [])
            if users:
                return users[0].get("PERSONAL_PHOTO")
            return None

    async def get_employee(self, user_id: str) -> dict[str, Any]:
        """Get employee info from Bitrix24.

        TODO: реализовать в Task 5.
        """
        raise NotImplementedError("Bitrix24Client.get_employee not yet implemented — Task 5")

    async def search_employees(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search employees in Bitrix24.

        TODO: реализовать в Task 5.
        """
        raise NotImplementedError("Bitrix24Client.search_employees not yet implemented — Task 5")

    async def create_task(self, title: str, description: str, **kwargs: Any) -> dict[str, Any]:
        """Create a task/ticket in Bitrix24.

        TODO: реализовать.
        """
        raise NotImplementedError("Bitrix24Client.create_task not yet implemented")

    async def list_tasks(self, user_id: str, status: str = "open") -> list[dict[str, Any]]:
        """List tasks/tickets for a user.

        TODO: реализовать.
        """
        raise NotImplementedError("Bitrix24Client.list_tasks not yet implemented")

    async def get_news(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get corporate news from Bitrix24.

        TODO: реализовать.
        """
        raise NotImplementedError("Bitrix24Client.get_news not yet implemented")
