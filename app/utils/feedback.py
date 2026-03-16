"""Feedback rating helpers."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import MessageFeedback


async def save_feedback(
    session: AsyncSession,
    message_id: UUID,
    user_id: str,
    rating: int,
    comment: str | None = None,
) -> MessageFeedback:
    """Save user feedback (👍/👎) for a chat message."""
    if rating not in (1, -1):
        raise ValueError(f"Rating must be 1 or -1, got {rating}")

    feedback = MessageFeedback(
        message_id=message_id,
        user_id=user_id,
        rating=rating,
        comment=comment,
    )
    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)
    return feedback
