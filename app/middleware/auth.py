from fastapi import Header, HTTPException

from app.schemas.chat import UserContext


async def get_current_user(authorization: str = Header(None)) -> UserContext:
    # TODO: реализовать в Task 2 (Keycloak JWT validation)
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UserContext(id="stub", name="Stub User")
