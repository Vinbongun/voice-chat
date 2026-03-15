from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from app.schemas.chat import UserContext


@dataclass
class AgentState:
    messages: Annotated[list[BaseMessage], add_messages] = field(default_factory=list)
    user: Optional[UserContext] = None
    session_id: str = ""
