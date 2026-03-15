from __future__ import annotations

# TODO: реализовать в Task 3 (LangGraph StateGraph + tool calling loop)
from typing import Any

from langgraph.graph import StateGraph

from app.agent.state import AgentState


def build_graph() -> Any:
    """Build and compile the LangGraph agent graph.

    Returns a compiled graph ready for invocation.
    TODO: implement full agent loop in Task 3.
    """
    graph = StateGraph(AgentState)
    # Placeholder: graph will have nodes added in Task 3
    raise NotImplementedError("Agent graph not yet implemented — Task 3")
