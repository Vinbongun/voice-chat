"""Tests for LangGraph agent graph — TDD RED phase written first.

Test cases:
1. test_build_graph_returns_compiled_graph
2. test_agent_routes_to_tools
3. test_agent_returns_final_response
4. test_agent_state_has_required_fields
"""
from __future__ import annotations

import dataclasses
from unittest.mock import AsyncMock, MagicMock

import pytest
from langchain_core.messages import AIMessage, HumanMessage


# ---------------------------------------------------------------------------
# 1. AgentState has required fields
# ---------------------------------------------------------------------------

def test_agent_state_has_required_fields():
    """AgentState dataclass must expose messages, user, and session_id fields."""
    from app.agent.state import AgentState

    fields = {f.name for f in dataclasses.fields(AgentState)}
    assert "messages" in fields
    assert "user" in fields
    assert "session_id" in fields


# ---------------------------------------------------------------------------
# 2. build_graph returns a compiled graph (has .invoke)
# ---------------------------------------------------------------------------

def test_build_graph_returns_compiled_graph(mocker):
    """build_graph(tools=[]) must return a compiled LangGraph graph with .invoke."""
    # Patch ChatOpenAI so we don't need real credentials at import/build time.
    mock_llm = MagicMock()
    mock_llm.bind_tools = MagicMock(return_value=mock_llm)
    mocker.patch("app.agent.graph.ChatOpenAI", return_value=mock_llm)

    from app.agent.graph import build_graph

    graph = build_graph(tools=[])
    assert hasattr(graph, "invoke"), "Compiled graph must have an 'invoke' method"


# ---------------------------------------------------------------------------
# 3. _should_continue routes to "tools" when last message has tool_calls
# ---------------------------------------------------------------------------

def test_agent_routes_to_tools(mocker):
    """_should_continue returns 'tools' when last AIMessage has tool_calls."""
    mock_llm = MagicMock()
    mock_llm.bind_tools = MagicMock(return_value=mock_llm)
    mocker.patch("app.agent.graph.ChatOpenAI", return_value=mock_llm)

    from app.agent.graph import _should_continue
    from app.agent.state import AgentState

    ai_msg_with_tool_call = AIMessage(
        content="",
        tool_calls=[{"name": "search_documents", "args": {}, "id": "call_1"}],
    )
    state = AgentState(
        messages=[HumanMessage(content="найди документ"), ai_msg_with_tool_call],
    )

    result = _should_continue(state)
    assert result == "tools", f"Expected 'tools', got {result!r}"


# ---------------------------------------------------------------------------
# 4. _should_continue returns "__end__" when last message has no tool_calls
# ---------------------------------------------------------------------------

def test_agent_returns_final_response(mocker):
    """_should_continue returns '__end__' when last AIMessage has no tool_calls."""
    mock_llm = MagicMock()
    mock_llm.bind_tools = MagicMock(return_value=mock_llm)
    mocker.patch("app.agent.graph.ChatOpenAI", return_value=mock_llm)

    from app.agent.graph import _should_continue
    from app.agent.state import AgentState

    ai_msg_no_tools = AIMessage(content="Вот ответ на ваш вопрос.", tool_calls=[])
    state = AgentState(
        messages=[HumanMessage(content="привет"), ai_msg_no_tools],
    )

    result = _should_continue(state)
    assert result == "__end__", f"Expected '__end__', got {result!r}"
