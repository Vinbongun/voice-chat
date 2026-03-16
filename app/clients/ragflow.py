from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


class RAGFlowClient:
    """REST API client for RAGFlow document search service."""

    def __init__(self) -> None:
        self.base_url = settings.RAGFLOW_BASE_URL
        self.api_key = settings.RAGFLOW_API_KEY

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=0.5, min=0.5, max=2))
    async def retrieve(
        self,
        query: str,
        dataset_ids: list[str] | None = None,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """Call RAGFlow /v1/retrieval endpoint and return a list of chunks."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/retrieval",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "question": query,
                    "dataset_ids": dataset_ids or [],
                    "top_k": top_k,
                    "similarity_threshold": 0.2,
                    "vector_similarity_weight": 0.3,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("chunks", [])
