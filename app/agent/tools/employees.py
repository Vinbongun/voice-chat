from __future__ import annotations

from typing import Any

from langchain_core.tools import tool


@tool
async def search_employees(
    query: str,
    department: str = "",
    city: str = "",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search employees by name, position, department, or city.

    Args:
        query: Free-text search query (name or position).
        department: Optional department filter.
        city: Optional city filter.
        limit: Maximum number of results.

    Returns:
        List of employee records.

    TODO: реализовать в Task 5 (Keycloak + Bitrix24 integration).
    """
    raise NotImplementedError("search_employees not yet implemented — Task 5")
