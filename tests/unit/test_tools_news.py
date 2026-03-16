"""Tests for search_news tool — TDD RED phase written first.

Test cases:
1. test_search_news_returns_news_list — mock DB returns News rows,
   tool returns list of dicts with title, content, published_at
2. test_search_news_empty_results — no rows → []
3. test_search_news_uses_fts — verify SQL contains to_tsvector/plainto_tsquery
4. test_search_news_limits_results — verify LIMIT in SQL
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_mock_row(data: dict) -> MagicMock:
    """Return a MagicMock that behaves like a RowMapping (dict-subscriptable)."""
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, key: data[key]
    return mock_row


def _make_mock_session(rows: list) -> AsyncMock:
    """Return a mock async context-manager session whose execute returns *rows*."""
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = rows

    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    return mock_session


# ---------------------------------------------------------------------------
# 1. search_news returns list[dict] with title, content, published_at
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_news_returns_news_list(mocker):
    """Tool must return list of dicts with title, content, published_at when DB returns rows."""
    from app.agent.tools.news import search_news

    row_data = {
        "id": "news-1",
        "title": "Новость компании",
        "content": "Содержание новости...",
        "published_at": "2026-03-16",
    }
    mock_session = _make_mock_session([_make_mock_row(row_data)])
    mocker.patch("app.agent.tools.news.async_session_maker", return_value=mock_session)

    result = await search_news.ainvoke({"query": "новость"})

    assert isinstance(result, list)
    assert len(result) == 1
    article = result[0]
    assert article["title"] == "Новость компании"
    assert article["content"] == "Содержание новости..."
    assert article["published_at"] == "2026-03-16"
    assert article["id"] == "news-1"


# ---------------------------------------------------------------------------
# 2. search_news returns empty list when no DB rows
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_news_empty_results(mocker):
    """Tool must return [] when DB returns no matching news rows."""
    from app.agent.tools.news import search_news

    mock_session = _make_mock_session([])
    mocker.patch("app.agent.tools.news.async_session_maker", return_value=mock_session)

    result = await search_news.ainvoke({"query": "НесуществующаяНовость"})

    assert result == []


# ---------------------------------------------------------------------------
# 3. search_news uses PostgreSQL full-text search (to_tsvector / plainto_tsquery)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_news_uses_fts(mocker):
    """Tool must execute a SQL query containing to_tsvector and plainto_tsquery."""
    from app.agent.tools.news import search_news

    mock_session = _make_mock_session([])
    mocker.patch("app.agent.tools.news.async_session_maker", return_value=mock_session)

    await search_news.ainvoke({"query": "объявление"})

    # session.execute must have been called exactly once
    mock_session.execute.assert_called_once()

    # Inspect the first positional argument (the SQLAlchemy text() object)
    call_args = mock_session.execute.call_args
    sql_arg = call_args.args[0] if call_args.args else call_args[0][0]

    # Convert to string to inspect the SQL text
    sql_text = str(sql_arg)
    assert "to_tsvector" in sql_text, f"Expected 'to_tsvector' in SQL, got: {sql_text}"
    assert "plainto_tsquery" in sql_text, f"Expected 'plainto_tsquery' in SQL, got: {sql_text}"


# ---------------------------------------------------------------------------
# 4. search_news limits results to 5
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_news_limits_results(mocker):
    """Tool must embed LIMIT 5 in the SQL query."""
    from app.agent.tools.news import search_news

    rows = [
        _make_mock_row({
            "id": f"news-{i}",
            "title": f"Новость {i}",
            "content": "Краткое содержание.",
            "published_at": "2026-03-16",
        })
        for i in range(7)
    ]
    mock_session = _make_mock_session(rows)
    mocker.patch("app.agent.tools.news.async_session_maker", return_value=mock_session)

    await search_news.ainvoke({"query": "новость"})

    # The SQL must contain "LIMIT 5"
    call_args = mock_session.execute.call_args
    sql_arg = call_args.args[0] if call_args.args else call_args[0][0]
    sql_text = str(sql_arg)
    assert "LIMIT 5" in sql_text or "limit 5" in sql_text.lower(), (
        f"Expected 'LIMIT 5' in SQL, got: {sql_text}"
    )
