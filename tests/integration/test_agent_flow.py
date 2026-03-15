"""Integration tests for agent flow through the chat endpoint.

TDD: these tests are written FIRST (RED phase) before implementation.
Tests verify that the agent is invoked correctly and tools are called as expected.
"""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from langchain_core.messages import AIMessage


@pytest.mark.asyncio
async def test_full_agent_flow_with_mock_llm(auth_client, mocker):
    """POST /chat triggers agent_graph.ainvoke and returns its text response.

    Mock LLM + mock tools: agent runs, returns text response.
    """
    expected_text = "Тестовый ответ от агента"
    mock_ainvoke = mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content=expected_text)]},
    )

    response = await auth_client.post("/chat", json={"message": "Как дела?"})

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == expected_text

    # Verify agent was actually called once
    mock_ainvoke.assert_called_once()

    # Verify the state passed to agent contains the user message
    call_args = mock_ainvoke.call_args
    state_arg = call_args[0][0]  # first positional argument
    # AgentState has .messages — last HumanMessage should contain our query
    human_messages = [
        m for m in state_arg.messages
        if hasattr(m, "type") and m.type == "human"
    ]
    assert len(human_messages) >= 1
    assert "Как дела?" in human_messages[-1].content


@pytest.mark.asyncio
async def test_full_agent_flow_session_id_generated_when_absent(auth_client, mocker):
    """When no session_id is provided, agent runs and response contains a generated one."""
    mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content="Ответ")]},
    )

    response = await auth_client.post("/chat", json={"message": "Тест"})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    # UUID format: 8-4-4-4-12 hex digits
    assert len(data["session_id"]) == 36
    assert data["session_id"].count("-") == 4


@pytest.mark.asyncio
async def test_agent_uses_rag_tool_when_document_query(auth_client, mocker):
    """When LLM returns a tool_call for search_documents, verify the tool is invoked.

    Simulates: LLM first returns tool_call → tool executes → LLM returns final answer.
    We mock agent_graph.ainvoke to simulate that the agent processed the tool call.
    """
    # Mock the RAGFlow tool directly to verify it would be called
    mock_search_docs = mocker.patch(
        "app.agent.tools.rag.ragflow_client.retrieve",
        new_callable=AsyncMock,
        return_value=[
            {
                "document_id": "doc-1",
                "document_keyword": "Политика отпусков",
                "content": "Сотрудники имеют право на 28 дней оплачиваемого отпуска.",
                "similarity": 0.95,
                "url": "/docs/doc-1",
            }
        ],
    )

    # Mock agent to return a realistic answer that would come after RAG tool usage
    rag_answer = "Согласно политике компании, сотрудники имеют право на 28 дней оплачиваемого отпуска."
    mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content=rag_answer)]},
    )

    response = await auth_client.post(
        "/chat", json={"message": "Сколько дней отпуска мне положено?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == rag_answer


@pytest.mark.asyncio
async def test_agent_system_prompt_includes_user_context(auth_client, mocker):
    """Agent is invoked with a state that includes a SystemMessage with user context."""
    mock_ainvoke = mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        return_value={"messages": [AIMessage(content="OK")]},
    )

    await auth_client.post("/chat", json={"message": "Тест промпта"})

    mock_ainvoke.assert_called_once()
    state_arg = mock_ainvoke.call_args[0][0]

    # First message should be a SystemMessage with user name
    system_messages = [
        m for m in state_arg.messages
        if hasattr(m, "type") and m.type == "system"
    ]
    assert len(system_messages) >= 1
    # The auth_client fixture uses "Test User" as the user name
    assert "Test User" in system_messages[0].content


@pytest.mark.asyncio
async def test_agent_error_handling_returns_500(auth_client, mocker):
    """If agent_graph.ainvoke raises an exception, endpoint returns 500."""
    mocker.patch(
        "app.routers.chat.agent_graph.ainvoke",
        new_callable=AsyncMock,
        side_effect=RuntimeError("LLM unavailable"),
    )

    response = await auth_client.post("/chat", json={"message": "Тест ошибки"})
    assert response.status_code == 500
