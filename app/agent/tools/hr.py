from __future__ import annotations

from typing import Any

from langchain_core.tools import tool


@tool
async def get_hr_info(topic: str, user_id: str) -> dict[str, Any]:
    """Get HR information for a specific topic and user.

    Args:
        topic: HR topic (e.g. "vacation", "sick_days", "benefits", "salary").
        user_id: Keycloak user ID for fetching personal HR data.

    Returns:
        HR information dict with relevant fields.

    TODO: реализовать (1С ЗУП integration).
    """
    raise NotImplementedError("get_hr_info not yet implemented")
