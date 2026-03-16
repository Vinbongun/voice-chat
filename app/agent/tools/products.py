from __future__ import annotations

from typing import Any

from langchain_core.tools import tool
from sqlalchemy import text

from app.clients.ragflow import RAGFlowClient
from app.db.database import async_session_maker
from app.schemas.chat import ProductAvailability, ProductCard

ragflow_client = RAGFlowClient()


@tool
async def search_products(query: str) -> list[dict[str, Any]]:
    """Search products in company catalog.

    Searches by name, brand, or description. Returns product cards with
    current prices and availability across branches.

    Args:
        query: Search query (product name, brand, or description)

    Returns:
        List of product cards with prices and availability
    """
    # Step 1: Semantic search in RAGFlow "Products" knowledge base
    chunks = await ragflow_client.retrieve(query=query, top_k=5)

    if not chunks:
        return []

    # Extract product IDs and basic data from RAGFlow results
    product_data: dict[str, dict[str, Any]] = {}
    for chunk in chunks:
        product_id = chunk.get("document_id", "")
        if product_id and product_id not in product_data:
            metadata = chunk.get("metadata", {}) or {}
            product_data[product_id] = {
                "id": product_id,
                "name": chunk.get("document_keyword", ""),
                "description": chunk.get("content", ""),
                "brand": metadata.get("brand", ""),
            }

    if not product_data:
        return []

    # Step 2: Enrich with prices from PostgreSQL
    product_ids = list(product_data.keys())

    async with async_session_maker() as session:
        prices_query = text("""
            SELECT p.id, p.name, p.brand, p.photo_url,
                   pp.branch_id, pp.branch_name, pp.price, pp.qty
            FROM products p
            LEFT JOIN product_prices pp ON pp.product_id = p.id
            WHERE p.id = ANY(:ids)
            ORDER BY p.id, pp.branch_name
        """)
        result = await session.execute(prices_query, {"ids": product_ids})
        rows = result.mappings().all()

    # Group rows by product_id; build availability list; first branch price = card price
    enriched: dict[str, dict[str, Any]] = {}
    for row in rows:
        pid = row["id"]
        if pid not in enriched:
            enriched[pid] = {
                "id": pid,
                "name": row["name"] or product_data.get(pid, {}).get("name", ""),
                "brand": row["brand"] or product_data.get(pid, {}).get("brand", ""),
                "description": product_data.get(pid, {}).get("description", ""),
                "photo_url": row["photo_url"] or "",
                "price": float(row["price"]) if row["price"] is not None else 0.0,
                "availability": [],
            }
        if row["branch_name"] is not None:
            enriched[pid]["availability"].append(
                ProductAvailability(
                    branch=row["branch_name"],
                    qty=row["qty"] if row["qty"] is not None else 0,
                )
            )

    # For products not found in DB, use RAGFlow data with no price / availability
    for pid, data in product_data.items():
        if pid not in enriched:
            enriched[pid] = {
                "id": pid,
                "name": data["name"],
                "brand": data.get("brand", ""),
                "description": data["description"],
                "photo_url": "",
                "price": None,
                "availability": [],
            }

    return [
        ProductCard(
            type="product",
            id=p["id"],
            name=p["name"],
            brand=p.get("brand", ""),
            description=p["description"],
            photo_url=p.get("photo_url", ""),
            price=p["price"],
            availability=p["availability"],
            url=f"/products/{p['id']}",
        ).model_dump()
        for p in enriched.values()
    ]
