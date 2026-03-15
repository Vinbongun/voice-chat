from __future__ import annotations

from typing import Any

import httpx

from app.config import settings


class RAGFlowClient:
    """REST API client for RAGFlow document search service.

    TODO: реализовать полностью в Task 4.
    """

    def __init__(self) -> None:
        self.base_url = settings.RAGFLOW_BASE_URL
        self.api_key = settings.RAGFLOW_API_KEY
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> RAGFlowClient:
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30.0,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search documents in RAGFlow.

        TODO: реализовать в Task 4.
        """
        raise NotImplementedError("RAGFlowClient.search not yet implemented — Task 4")
