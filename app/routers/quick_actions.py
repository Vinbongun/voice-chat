from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.schemas.chat import QuickActionRequest, QuickActionResponse, UserContext

router = APIRouter(prefix="/chat", tags=["chat"])

# Quick action → canned message for the agent
QUICK_ACTION_MESSAGES = {
    "my_vacation": "Сколько у меня осталось дней отпуска?",
    "my_tickets": "Покажи мои активные заявки",
    "find_employee": "Помоги найти сотрудника",
    "find_product": "Найди товар в каталоге",
    "it_help": "Мне нужна помощь с IT проблемой",
}


@router.post("/quick-action", response_model=QuickActionResponse)
async def quick_action(
    request: QuickActionRequest,
    user: UserContext = Depends(get_current_user),
) -> QuickActionResponse:
    """Handle predefined quick actions."""
    if request.action not in QUICK_ACTION_MESSAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown action '{request.action}'. Valid: {list(QUICK_ACTION_MESSAGES)}",
        )

    message = QUICK_ACTION_MESSAGES[request.action]
    # Apply any payload params to the message
    if request.payload:
        for key, val in request.payload.items():
            message = message.replace(f"{{{key}}}", str(val))

    return QuickActionResponse(
        result={"action": request.action, "message": message},
        message=message,
    )
