from __future__ import annotations

from typing import Any

import httpx

from app.config import settings


class UITClient:
    """1С УИТ (Upravleniye Informatsionnymi Tekhnologiyami) REST API client.

    Used for products, services catalog, and IT asset management.
    TODO: реализовать полностью.
    """

    def __init__(self) -> None:
        self.api_url = settings.UIT_API_URL
        self.api_token = settings.UIT_API_TOKEN
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> UITClient:
        self._client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={"Authorization": f"Bearer {self.api_token}"},
            timeout=30.0,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

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
