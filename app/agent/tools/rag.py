from __future__ import annotations

from typing import Any

from langchain_core.tools import tool


@tool
async def search_documents(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Search corporate documents via RAGFlow.

    Args:
        query: Search query string.
        top_k: Maximum number of results to return.

    Returns:
        List of document chunks with title, snippet, url, and relevance score.

    TODO: реализовать в Task 4 (RAGFlow REST API integration).
    """
    raise NotImplementedError("search_documents not yet implemented — Task 4")
