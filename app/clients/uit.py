from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


class UITClient:
    """1С УИТ IT service desk API client."""

    def __init__(self) -> None:
        self.base_url = settings.UIT_API_URL
        self.api_token = settings.UIT_API_TOKEN

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def create_ticket(
        self,
        user_id: str,
        title: str,
        description: str,
        category: str = "IT",
        priority: str = "normal",
    ) -> dict[str, Any]:
        """Create a new support ticket."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tickets",
                headers=self._headers(),
                json={
                    "user_id": user_id,
                    "title": title,
                    "description": description,
                    "category": category,
                    "priority": priority,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def list_tickets(self, user_id: str, status: str = "active") -> list[dict[str, Any]]:
        """List tickets for a user."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tickets",
                headers=self._headers(),
                params={"user_id": user_id, "status": status},
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("tickets", [])

    async def search_products(self, query: str, category: str = "", limit: int = 10) -> list[dict[str, Any]]:
        """Search products in 1C UIT catalog.

        TODO: реализовать.
        """
        raise NotImplementedError("UITClient.search_products not yet implemented")

    async def get_product(self, product_id: str) -> dict[str, Any]:
        """Get product details from 1C UIT.

        TODO: реализовать.
        """
        raise NotImplementedError("UITClient.get_product not yet implemented")
