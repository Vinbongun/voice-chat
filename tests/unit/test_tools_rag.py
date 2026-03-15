"""Tests for search_documents tool and RAGFlowClient — TDD RED phase written first.

Test cases:
1. test_search_documents_returns_document_sources — mock RAGFlow client returns chunks,
   tool returns list[dict] shaped like DocumentSource
2. test_search_documents_empty_results — RAGFlow returns [] → tool returns []
3. test_search_documents_calls_ragflow_with_correct_params — verify retrieve called
   with query and top_k=5
4. test_ragflow_client_builds_correct_request — unit test for RAGFlowClient: correct
   URL, Authorization header, request body
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest


# ---------------------------------------------------------------------------
# 1. search_documents returns list of DocumentSource-shaped dicts
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_documents_returns_document_sources(mocker):
    """Tool must return list[dict] with title, url, snippet when RAGFlow returns chunks."""
    from app.agent.tools.rag import search_documents

    fake_chunks = [
        {
            "document_keyword": "Регламент командировок",
            "document_id": "doc-123",
            "content": "Для оформления командировки необходимо...",
            "page_num": 3,
            "url": "/docs/doc-123",
        }
    ]
    mocker.patch("app.agent.tools.rag.ragflow_client.retrieve", AsyncMock(return_value=fake_chunks))

    result = await search_documents.ainvoke({"query": "как оформить командировку"})

    assert isinstance(result, list)
    assert len(result) == 1
    item = result[0]
    assert item["title"] == "Регламент командировок"
    assert item["url"] == "/docs/doc-123"
    assert "Для оформления командировки" in item["snippet"]


# ---------------------------------------------------------------------------
# 2. search_documents returns empty list when RAGFlow returns no chunks
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_documents_empty_results(mocker):
    """Tool must return [] when RAGFlow retrieves no chunks."""
    from app.agent.tools.rag import search_documents

    mocker.patch("app.agent.tools.rag.ragflow_client.retrieve", AsyncMock(return_value=[]))

    result = await search_documents.ainvoke({"query": "несуществующий документ"})

    assert result == []


# ---------------------------------------------------------------------------
# 3. search_documents calls RAGFlow retrieve with correct params
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_documents_calls_ragflow_with_correct_params(mocker):
    """Tool must call ragflow_client.retrieve(query=..., top_k=5)."""
    from app.agent.tools.rag import search_documents

    mock_retrieve = AsyncMock(return_value=[])
    mocker.patch("app.agent.tools.rag.ragflow_client.retrieve", mock_retrieve)

    await search_documents.ainvoke({"query": "отпуск"})

    mock_retrieve.assert_called_once_with(query="отпуск", top_k=5)


# ---------------------------------------------------------------------------
# 4. RAGFlowClient.retrieve builds correct HTTP request
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ragflow_client_builds_correct_request(mocker):
    """RAGFlowClient.retrieve must POST to /v1/retrieval with correct headers and body."""
    from app.clients.ragflow import RAGFlowClient

    # Build a mock httpx.AsyncClient context manager
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "chunks": [
                {
                    "document_keyword": "Тест",
                    "document_id": "doc-999",
                    "content": "Тестовый контент",
                    "page_num": 1,
                    "url": "/docs/doc-999",
                }
            ]
        }
    }
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = AsyncMock(return_value=mock_response)

    mocker.patch("app.clients.ragflow.httpx.AsyncClient", return_value=mock_client)

    client = RAGFlowClient()
    # Temporarily set known values so we can assert on them
    client.base_url = "http://ragflow-test:9380"
    client.api_key = "test-api-key"

    chunks = await client.retrieve(query="тест запрос", top_k=5)

    # Verify POST was called
    mock_client.post.assert_called_once()
    call_kwargs = mock_client.post.call_args

    # URL
    url_arg = call_kwargs.args[0] if call_kwargs.args else call_kwargs.kwargs.get("url", "")
    assert "/v1/retrieval" in url_arg, f"Expected /v1/retrieval in URL, got: {url_arg}"

    # Headers
    headers = call_kwargs.kwargs.get("headers", {})
    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer test-api-key"

    # Request body
    body = call_kwargs.kwargs.get("json", {})
    assert body["question"] == "тест запрос"
    assert body["top_k"] == 5

    # Return value
    assert len(chunks) == 1
    assert chunks[0]["document_keyword"] == "Тест"
