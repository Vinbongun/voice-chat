from __future__ import annotations

import logging
from typing import Any

from langchain_core.tools import tool

from app.clients.ragflow import RAGFlowClient
from app.schemas.chat import DocumentSource

logger = logging.getLogger(__name__)
ragflow_client = RAGFlowClient()


@tool
async def search_documents(query: str) -> list[dict[str, Any]]:
    """Search company documents using RAGFlow knowledge base.

    Use this tool to find information in company policies, regulations,
    instructions, and other official documents.

    Args:
        query: The search query in Russian

    Returns:
        List of relevant document excerpts with source information
    """
    try:
        chunks = await ragflow_client.retrieve(query=query, top_k=5)
    except Exception as exc:
        logger.warning("RAGFlow unavailable: %s", exc)
        return []

    results = []
    for chunk in chunks:
        results.append(
            DocumentSource(
                title=chunk.get("document_keyword", chunk.get("document_id", "Unknown")),
                url=chunk.get("url", f"/docs/{chunk.get('document_id', '')}"),
                snippet=chunk.get("content", ""),
                relevance=chunk.get("similarity", 0.0),
            ).model_dump()
        )

    return results
