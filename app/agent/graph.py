from __future__ import annotations

from typing import Literal

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.state import AgentState
from app.config import settings


def _should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    """Route to tools if last message has tool_calls, else end."""
    last_message = state.messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "__end__"


def build_graph(tools: list = None):
    """Build and compile the LangGraph agent."""
    if tools is None:
        tools = []

    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        base_url=settings.LLM_BASE_URL or None,
        api_key=settings.OPENAI_API_KEY or "placeholder",
    )

    if tools:
        llm = llm.bind_tools(tools)

    tool_node = ToolNode(tools)

    async def call_model(state: AgentState) -> dict:
        response = await llm.ainvoke(state.messages)
        return {"messages": [response]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        _should_continue,
        {"tools": "tools", "__end__": END},
    )
    graph.add_edge("tools", "agent")

    return graph.compile()
