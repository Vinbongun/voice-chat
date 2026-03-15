"""
TDD tests for Keycloak JWT auth middleware.
Tests are written FIRST (RED phase), implementation follows (GREEN phase).
"""
import pytest
from fastapi import HTTPException
from jose import JWTError, ExpiredSignatureError


# Sample Keycloak JWT payload
SAMPLE_PAYLOAD = {
    "sub": "user-uuid",
    "preferred_username": "ivanov",
    "name": "Иван Иванов",
    "email": "ivanov@company.ru",
    "realm_access": {"roles": []},
    "attributes": {
        "position": ["Разработчик"],
        "department": ["IT"],
        "city": ["Москва"],
    },
}


@pytest.mark.asyncio
async def test_no_token_raises_401():
    """Request without Authorization header must raise HTTPException 401."""
    from app.middleware.auth import get_current_user

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(authorization=None)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token_raises_401(mocker):
    """Invalid JWT token must raise HTTPException 401."""
    from app.middleware.auth import get_current_user

    mocker.patch("app.middleware.auth.jwt.decode", side_effect=JWTError("bad token"))

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(authorization="Bearer invalid.token.here")

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_expired_token_raises_401(mocker):
    """Expired JWT token must raise HTTPException 401."""
    from app.middleware.auth import get_current_user

    mocker.patch(
        "app.middleware.auth.jwt.decode",
        side_effect=ExpiredSignatureError("token expired"),
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(authorization="Bearer expired.token.here")

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_valid_token_returns_user_context(mocker):
    """Valid JWT must return a UserContext object."""
    from app.middleware.auth import get_current_user
    from app.schemas.chat import UserContext
    from app.middleware import auth as auth_module

    mocker.patch("app.middleware.auth.jwt.decode", return_value=SAMPLE_PAYLOAD)

    result = await get_current_user(authorization="Bearer valid.token.here")

    assert isinstance(result, UserContext)
    assert auth_module.ALGORITHM == "RS256"


@pytest.mark.asyncio
async def test_user_context_fields_extracted(mocker):
    """JWT claims are correctly extracted into UserContext fields."""
    from app.middleware.auth import get_current_user

    mocker.patch("app.middleware.auth.jwt.decode", return_value=SAMPLE_PAYLOAD)

    result = await get_current_user(authorization="Bearer valid.token.here")

    assert result.id == "user-uuid"
    assert result.name == "Иван Иванов"
    assert result.position == "Разработчик"
    assert result.department == "IT"
    assert result.city == "Москва"


@pytest.mark.asyncio
async def test_malformed_bearer_raises_401():
    """Wrong casing or empty token after Bearer."""
    from app.middleware.auth import get_current_user

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(authorization="bearer valid.token.here")
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_missing_sub_raises_401(mocker):
    """JWT without sub claim should raise 401."""
    from app.middleware.auth import get_current_user

    payload_no_sub = {"name": "Test", "attributes": {}}
    mocker.patch("app.middleware.auth.jwt.decode", return_value=payload_no_sub)
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(authorization="Bearer fake.token")
    assert exc_info.value.status_code == 401
