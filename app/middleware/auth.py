from jose import jwt, JWTError
from fastapi import Header, HTTPException

from app.schemas.chat import UserContext

ALGORITHM = "RS256"


async def get_current_user(authorization: str = Header(None)) -> UserContext:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        # Decode without signature verification for now.
        # In production: fetch JWKS from Keycloak and verify.
        payload = jwt.decode(
            token,
            key="",  # will be configured in Phase 3
            algorithms=[ALGORITHM],
            options={"verify_signature": False, "verify_exp": True},
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    attributes = payload.get("attributes", {})

    return UserContext(
        id=payload.get("sub", ""),
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
