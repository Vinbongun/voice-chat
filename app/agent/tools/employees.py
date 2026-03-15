from __future__ import annotations

from langchain_core.tools import tool
from sqlalchemy import text

from app.db.database import async_session_maker
from app.schemas.chat import EmployeeCard


@tool
async def search_employees(query: str) -> list[dict]:
    """Search employees in the company directory.

    Use this tool to find employees by name, position, or department.

    Args:
        query: Search query (employee name, position, or department)

    Returns:
        List of employee cards with contact information
    """
    async with async_session_maker() as session:
        # Full-text search using PostgreSQL ts_vector
        fts_query = text("""
            SELECT id, name, position, department, phone, email, photo_url, city
            FROM employees
            WHERE to_tsvector('russian', name || ' ' || COALESCE(position, '') || ' ' || COALESCE(department, ''))
                  @@ plainto_tsquery('russian', :query)
            ORDER BY synced_at DESC
            LIMIT 5
        """)
        result = await session.execute(fts_query, {"query": query})
        rows = result.mappings().all()

        return [
            EmployeeCard(
                type="employee",
                id=row["id"],
                name=row["name"] or "",
                position=row["position"] or "",
                department=row["department"] or "",
                phone=row["phone"] or "",
                email=row["email"] or "",
                photo_url=row["photo_url"] or "",
                city=row["city"] or "",
            ).model_dump()
            for row in rows
        ]
