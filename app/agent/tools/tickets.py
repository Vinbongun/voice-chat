from __future__ import annotations

from langchain_core.tools import tool

from app.clients.uit import UITClient

uit_client = UITClient()


@tool
async def create_ticket(
    user_id: str,
    title: str,
    description: str,
    category: str = "IT",
) -> dict:
    """Create a support ticket in 1С УИТ service desk.

    Use this tool ONLY after explicitly confirming details with the user.
    Always ask for title and description before calling this tool.

    Args:
        user_id: Employee ID (from JWT token)
        title: Short ticket title
        description: Detailed description of the issue
        category: Ticket category (IT, HR, Facilities, etc.)

    Returns:
        Ticket creation result with ticket_id and status
    """
    result = await uit_client.create_ticket(
        user_id=user_id,
        title=title,
        description=description,
        category=category,
    )
    return {
        "ticket_id": result.get("id", result.get("ticket_id", "")),
        "status": result.get("status", "created"),
        "message": f"Заявка #{result.get('id', '')} успешно создана",
        "url": result.get("url", ""),
    }


@tool
async def list_tickets(user_id: str, status: str = "active") -> list[dict]:
    """List support tickets for the current user.

    Args:
        user_id: Employee ID (from JWT token)
        status: Filter by status: active, closed, all

    Returns:
        List of tickets with id, title, status, created_at
    """
    tickets = await uit_client.list_tickets(user_id=user_id, status=status)
    return [
        {
            "id": t.get("id", ""),
            "title": t.get("title", ""),
            "status": t.get("status", ""),
            "category": t.get("category", ""),
            "created_at": t.get("created_at", ""),
            "updated_at": t.get("updated_at", ""),
        }
        for t in tickets
    ]
