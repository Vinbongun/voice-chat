from langchain_core.tools import tool
from sqlalchemy import text
from app.db.database import async_session_maker


@tool
async def search_news(query: str) -> list[dict]:
    """Search company news and announcements.

    Use this tool to find recent news, announcements, and updates from the company.

    Args:
        query: Search query in Russian

    Returns:
        List of news articles matching the query
    """
    async with async_session_maker() as session:
        fts_query = text("""
            SELECT id::text, title, content, published_at::text
            FROM news
            WHERE to_tsvector('russian', title || ' ' || content)
                  @@ plainto_tsquery('russian', :query)
            ORDER BY published_at DESC
            LIMIT 5
        """)
        result = await session.execute(fts_query, {"query": query})
        rows = result.mappings().all()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"][:500] + "..." if len(row["content"]) > 500 else row["content"],
                "published_at": row["published_at"],
            }
            for row in rows
        ]
