from __future__ import annotations

from typing import Any

from langchain_core.tools import tool


@tool
async def search_products(query: str, category: str = "", limit: int = 10) -> list[dict[str, Any]]:
    """Search company products and services catalog.

    Args:
        query: Free-text search query.
        category: Optional product category filter.
        limit: Maximum number of results.

    Returns:
        List of product records from 1C UIT.

    TODO: реализовать (1С УИТ integration).
    """
    raise NotImplementedError("search_products not yet implemented")
