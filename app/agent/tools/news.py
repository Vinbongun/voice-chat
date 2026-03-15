from __future__ import annotations

from typing import Any

from langchain_core.tools import tool


@tool
async def search_news(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Search corporate news and announcements.

    Args:
        query: Search query string.
        limit: Maximum number of results.

    Returns:
        List of news items with title, body, date, and url.

    TODO: реализовать (Bitrix24 news feed integration).
    """
    raise NotImplementedError("search_news not yet implemented")
