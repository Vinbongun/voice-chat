from __future__ import annotations

from typing import Any

from langchain_core.tools import tool


@tool
async def create_ticket(
    title: str,
    description: str,
    category: str = "general",
    priority: str = "normal",
    user_id: str = "",
) -> dict[str, Any]:
    """Create a support ticket in Bitrix24.

    Args:
        title: Ticket title/subject.
        description: Detailed description of the issue.
        category: Ticket category (e.g. "it", "hr", "facilities", "general").
        priority: Priority level ("low", "normal", "high", "urgent").
        user_id: ID of the user creating the ticket.

    Returns:
        Created ticket info with id and url.

    TODO: реализовать (Bitrix24 REST API integration).
    """
    raise NotImplementedError("create_ticket not yet implemented")


@tool
async def list_tickets(user_id: str, status: str = "open", limit: int = 10) -> list[dict[str, Any]]:
    """List support tickets for a user.

    Args:
        user_id: User ID to filter tickets.
        status: Ticket status filter ("open", "closed", "all").
        limit: Maximum number of results.

    Returns:
        List of ticket records.

    TODO: реализовать (Bitrix24 REST API integration).
    """
    raise NotImplementedError("list_tickets not yet implemented")
