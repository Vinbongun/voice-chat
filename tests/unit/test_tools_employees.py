"""Tests for search_employees tool — TDD RED phase written first.

Test cases:
1. test_search_employees_returns_employee_cards — mock DB session returns Employee rows,
   tool returns list[dict] shaped like EmployeeCard
2. test_search_employees_empty_results — no employees found → []
3. test_search_employees_queries_with_fts — verify SQLAlchemy query uses
   to_tsvector / plainto_tsquery for full-text search
4. test_search_employees_limits_results — results are limited (max 5)
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, call

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
# 1. search_employees returns list[dict] shaped like EmployeeCard
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_employees_returns_employee_cards(mocker):
    """Tool must return list of EmployeeCard-shaped dicts when DB returns rows."""
    from app.agent.tools.employees import search_employees

    row_data = {
        "id": "user-1",
        "name": "Иван Иванов",
        "position": "Разработчик",
        "department": "IT",
        "phone": "+7 999 000-00-00",
        "email": "ivan@company.ru",
        "photo_url": "https://cdn.example.com/photo.jpg",
        "city": "Москва",
    }
    mock_session = _make_mock_session([_make_mock_row(row_data)])
    mocker.patch("app.agent.tools.employees.async_session_maker", return_value=mock_session)

    result = await search_employees.ainvoke({"query": "Иванов"})

    assert isinstance(result, list)
    assert len(result) == 1
    card = result[0]
    assert card["type"] == "employee"
    assert card["id"] == "user-1"
    assert card["name"] == "Иван Иванов"
    assert card["position"] == "Разработчик"
    assert card["department"] == "IT"
    assert card["phone"] == "+7 999 000-00-00"
    assert card["email"] == "ivan@company.ru"
    assert card["photo_url"] == "https://cdn.example.com/photo.jpg"
    assert card["city"] == "Москва"


# ---------------------------------------------------------------------------
# 2. search_employees returns empty list when no DB rows
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_employees_empty_results(mocker):
    """Tool must return [] when DB returns no matching employees."""
    from app.agent.tools.employees import search_employees

    mock_session = _make_mock_session([])
    mocker.patch("app.agent.tools.employees.async_session_maker", return_value=mock_session)

    result = await search_employees.ainvoke({"query": "НесуществующийСотрудник"})

    assert result == []


# ---------------------------------------------------------------------------
# 3. search_employees uses PostgreSQL full-text search (to_tsvector / plainto_tsquery)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_employees_queries_with_fts(mocker):
    """Tool must execute a SQL query containing to_tsvector and plainto_tsquery."""
    from app.agent.tools.employees import search_employees

    mock_session = _make_mock_session([])
    mocker.patch("app.agent.tools.employees.async_session_maker", return_value=mock_session)

    await search_employees.ainvoke({"query": "разработчик"})

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
# 4. search_employees limits results to 5
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_employees_limits_results(mocker):
    """Tool must embed LIMIT 5 in the SQL query and return at most 5 results."""
    from app.agent.tools.employees import search_employees

    # Provide 7 rows to ensure the SQL itself carries the LIMIT (not Python slicing)
    rows = [
        _make_mock_row({
            "id": f"user-{i}",
            "name": f"Сотрудник {i}",
            "position": "Инженер",
            "department": "IT",
            "phone": "",
            "email": "",
            "photo_url": "",
            "city": "",
        })
        for i in range(7)
    ]
    mock_session = _make_mock_session(rows)
    mocker.patch("app.agent.tools.employees.async_session_maker", return_value=mock_session)

    await search_employees.ainvoke({"query": "Сотрудник"})

    # The SQL must contain "LIMIT 5"
    call_args = mock_session.execute.call_args
    sql_arg = call_args.args[0] if call_args.args else call_args[0][0]
    sql_text = str(sql_arg)
    assert "LIMIT 5" in sql_text or "limit 5" in sql_text.lower(), (
        f"Expected 'LIMIT 5' in SQL, got: {sql_text}"
    )
