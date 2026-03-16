"""Tests for search_products tool — TDD RED phase written first.

Test cases:
1. test_search_products_returns_product_cards — mock RAGFlow + DB, returns list
   with correct ProductCard fields (type, id, name, brand, description,
   photo_url, price, availability, url)
2. test_search_products_empty_ragflow_results — RAGFlow returns [] → tool returns []
3. test_search_products_enriches_with_prices — verify DB query called with
   product_ids from RAGFlow results
4. test_search_products_handles_missing_prices — product in RAGFlow but no
   prices in DB → availability == [] and price is None or 0.0
"""
from __future__ import annotations

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_mock_row(data: dict) -> MagicMock:
    """Return a MagicMock that behaves like a RowMapping (dict-subscriptable)."""
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, key: data[key]
    # Also support .get() as mappings do
    mock_row.get = lambda key, default=None: data.get(key, default)
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


# RAGFlow chunk shape for products
_RAGFLOW_CHUNK = {
    "document_keyword": "Корм Royal Canin Adult Maxi",
    "document_id": "prod-001",
    "content": "Сухой корм для взрослых собак крупных пород.",
    "metadata": {"brand": "Royal Canin"},
}

# DB rows for product_prices JOIN products
_DB_ROW = {
    "id": "prod-001",
    "name": "Корм Royal Canin Adult Maxi",
    "brand": "Royal Canin",
    "photo_url": "https://cdn.example.com/rc_adult.jpg",
    "description": "Сухой корм для взрослых собак крупных пород.",
    "branch_id": "msk",
    "branch_name": "Москва",
    "price": Decimal("1890.00"),
    "qty": 45,
}


# ---------------------------------------------------------------------------
# 1. search_products returns list[dict] shaped like ProductCard
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_products_returns_product_cards(mocker):
    """Tool must return list of ProductCard-shaped dicts when RAGFlow and DB return data."""
    from app.agent.tools.products import search_products

    mocker.patch(
        "app.agent.tools.products.ragflow_client.retrieve",
        new=AsyncMock(return_value=[_RAGFLOW_CHUNK]),
    )
    mock_session = _make_mock_session([_make_mock_row(_DB_ROW)])
    mocker.patch("app.agent.tools.products.async_session_maker", return_value=mock_session)

    result = await search_products.ainvoke({"query": "корм для собак"})

    assert isinstance(result, list)
    assert len(result) == 1
    card = result[0]

    # Fields required by ProductCard schema
    assert card["type"] == "product"
    assert card["id"] == "prod-001"
    assert card["name"] == "Корм Royal Canin Adult Maxi"
    assert isinstance(card["brand"], str)
    assert isinstance(card["description"], str)
    assert isinstance(card["photo_url"], str)
    # price comes from DB row (first availability entry)
    assert card["price"] == 1890.0
    # availability is a list of branch/qty dicts
    assert isinstance(card["availability"], list)
    assert len(card["availability"]) >= 1
    avail_entry = card["availability"][0]
    assert "branch" in avail_entry
    assert "qty" in avail_entry
    # url is /products/<id>
    assert card["url"] == "/products/prod-001"


# ---------------------------------------------------------------------------
# 2. search_products returns [] when RAGFlow returns empty list
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_products_empty_ragflow_results(mocker):
    """Tool must return [] when RAGFlow returns no chunks."""
    from app.agent.tools.products import search_products

    mocker.patch(
        "app.agent.tools.products.ragflow_client.retrieve",
        new=AsyncMock(return_value=[]),
    )
    # DB should NOT be called at all — no need to mock it
    result = await search_products.ainvoke({"query": "несуществующий товар"})

    assert result == []


# ---------------------------------------------------------------------------
# 3. search_products enriches results with DB prices using product_ids from RAGFlow
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_products_enriches_with_prices(mocker):
    """Tool must query DB using the product_ids extracted from RAGFlow chunks."""
    from app.agent.tools.products import search_products

    chunks = [
        {
            "document_keyword": "Корм Royal Canin Adult Maxi",
            "document_id": "prod-001",
            "content": "Описание продукта",
        },
        {
            "document_keyword": "Лакомство Dreamies",
            "document_id": "prod-002",
            "content": "Описание лакомства",
        },
    ]
    mocker.patch(
        "app.agent.tools.products.ragflow_client.retrieve",
        new=AsyncMock(return_value=chunks),
    )

    db_rows = [
        _make_mock_row({
            "id": "prod-001",
            "name": "Корм Royal Canin Adult Maxi",
            "brand": "Royal Canin",
            "photo_url": "",
            "description": "Описание продукта",
            "branch_id": "msk",
            "branch_name": "Москва",
            "price": Decimal("1890.00"),
            "qty": 45,
        }),
        _make_mock_row({
            "id": "prod-002",
            "name": "Лакомство Dreamies",
            "brand": "Dreamies",
            "photo_url": "",
            "description": "Описание лакомства",
            "branch_id": "msk",
            "branch_name": "Москва",
            "price": Decimal("120.00"),
            "qty": 200,
        }),
    ]
    mock_session = _make_mock_session(db_rows)
    mocker.patch("app.agent.tools.products.async_session_maker", return_value=mock_session)

    result = await search_products.ainvoke({"query": "корм"})

    # DB must have been queried
    mock_session.execute.assert_called_once()

    # Inspect the SQL to verify it uses ANY(:ids) or similar multi-product query
    call_args = mock_session.execute.call_args
    sql_arg = call_args.args[0] if call_args.args else call_args[0][0]
    sql_text = str(sql_arg)
    # The query should reference both tables
    assert "product_prices" in sql_text.lower() or "products" in sql_text.lower(), (
        f"Expected SQL to reference products/product_prices, got: {sql_text}"
    )

    # Both products must appear in the result
    ids_in_result = {card["id"] for card in result}
    assert "prod-001" in ids_in_result
    assert "prod-002" in ids_in_result


# ---------------------------------------------------------------------------
# 4. search_products handles products with no DB prices gracefully
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_products_handles_missing_prices(mocker):
    """Product found in RAGFlow but absent from DB → availability == [] and price is None."""
    from app.agent.tools.products import search_products

    mocker.patch(
        "app.agent.tools.products.ragflow_client.retrieve",
        new=AsyncMock(return_value=[_RAGFLOW_CHUNK]),
    )
    # DB returns empty — product not found in products/product_prices
    mock_session = _make_mock_session([])
    mocker.patch("app.agent.tools.products.async_session_maker", return_value=mock_session)

    result = await search_products.ainvoke({"query": "корм"})

    assert isinstance(result, list)
    assert len(result) == 1
    card = result[0]
    assert card["id"] == "prod-001"
    # availability is empty when no DB row exists
    assert card["availability"] == []
    # price defaults to None when no DB row exists
    assert card["price"] is None or card["price"] == 0.0
