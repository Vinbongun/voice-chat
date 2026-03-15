from __future__ import annotations

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user
from app.schemas.chat import QuickActionRequest, QuickActionResponse, UserContext

router = APIRouter(prefix="/chat", tags=["quick-actions"])


@router.post("/quick-action", response_model=QuickActionResponse)
async def quick_action(
    request: QuickActionRequest,
    current_user: UserContext = Depends(get_current_user),
) -> QuickActionResponse:
    """Execute a quick action (e.g. create ticket, get vacation balance).

    TODO: реализовать полностью в последующих задачах.
    """
    raise NotImplementedError("POST /chat/quick-action not yet implemented")
