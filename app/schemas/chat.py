from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class UserContext(BaseModel):
    id: str
    name: str
    position: str = ""
    department: str = ""
    city: str = ""


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[UUID] = None


class DocumentSource(BaseModel):
    title: str
    url: str = ""
    snippet: str = ""
    relevance: float = 0.0


class EmployeeCard(BaseModel):
    type: str = "employee"
    id: str
    name: str
    position: str = ""
    department: str = ""
    phone: str = ""
    email: str = ""
    photo_url: str = ""
    city: str = ""


class ProductAvailability(BaseModel):
    branch: str
    qty: int = 0


class ProductCard(BaseModel):
    type: str = "product"
    id: str
    name: str
    brand: str = ""
    description: str = ""
    photo_url: str = ""
    price: Optional[float] = None
    availability: list[ProductAvailability] = []
    url: str = ""


class HRInfoCard(BaseModel):
    type: str = "hr_info"
    title: str
    content: str
    fields: dict[str, Any] = {}


class ActionButton(BaseModel):
    label: str
    action: str
    payload: dict[str, Any] = {}


class ChatResponse(BaseModel):
    session_id: UUID
    message_id: UUID
    text: str
    sources: list[DocumentSource] = []
    cards: list[EmployeeCard | ProductCard | HRInfoCard] = []
    actions: list[ActionButton] = []


class SSEEvent(BaseModel):
    type: str  # "delta" | "sources" | "cards" | "done" | "error"
    delta: Optional[str] = None
    sources: Optional[list[DocumentSource]] = None
    cards: Optional[list[EmployeeCard | ProductCard | HRInfoCard]] = None
    message_id: Optional[str] = None
    session_id: Optional[str] = None


class QuickActionRequest(BaseModel):
    action: str
    payload: dict[str, Any] = {}


class QuickActionResponse(BaseModel):
    result: dict[str, Any] = {}
    message: str = ""


class FeedbackRequest(BaseModel):
    message_id: UUID
    rating: int  # 1 (👍) or -1 (👎)
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    success: bool
    message: str
