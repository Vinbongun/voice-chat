from typing import Optional

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Header, Query, HTTPException

from app.schemas.chat import UserContext
from app.config import settings

ALGORITHM = "RS256"

_DEV_USER = UserContext(
    id="dev-user",
    name="Dev User",
    position="",
    department="",
    city="",
)


async def get_current_user(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None),
) -> UserContext:
    # Dev bypass — set DEV_AUTH_BYPASS=true in .env to skip JWT (never use in prod)
    if settings.DEV_AUTH_BYPASS:
        return _DEV_USER

    # EventSource (SSE) cannot send custom headers, so accept token via query param
    raw_token = None
    if authorization and authorization.startswith("Bearer "):
        raw_token = authorization.removeprefix("Bearer ").strip()
    elif token:
        raw_token = token

    if not raw_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token_str = raw_token

    try:
        # SECURITY: verify_signature=False is for development only.
        # Set KEYCLOAK_PUBLIC_KEY in config to enable signature verification (Phase 3).
        payload = jwt.decode(
            token_str,
            key="",  # will be configured in Phase 3
            algorithms=[ALGORITHM],
            options={"verify_signature": False, "verify_exp": True},
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    user_id = payload.get("sub", "")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing sub claim")

    attributes = payload.get("attributes", {})

    return UserContext(
        id=user_id,
        name=payload.get("name") or payload.get("preferred_username", ""),
        position=_extract_attr(attributes, "position"),
        department=_extract_attr(attributes, "department"),
        city=_extract_attr(attributes, "city"),
    )


def _extract_attr(attributes: dict, key: str) -> str:
    """Extract first value from Keycloak attribute list."""
    value = attributes.get(key, [])
    if isinstance(value, list):
        return value[0] if value else ""
    return str(value) if value else ""
