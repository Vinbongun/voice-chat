from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


@dataclass
class UserContext:
    id: str
    name: str
    position: str = ""
    department: str = ""
    city: str = ""


@dataclass
class AgentState:
    messages: Annotated[list[BaseMessage], add_messages] = field(default_factory=list)
    user: Optional[UserContext] = None
    session_id: str = ""
