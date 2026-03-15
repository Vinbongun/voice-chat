from __future__ import annotations

from typing import Any

from app.config import settings


class KeycloakClient:
    """Keycloak Admin API client for user management and JWT verification.

    TODO: реализовать полностью в Task 2 и Task 5.
    """

    def __init__(self) -> None:
        self.server_url = settings.KEYCLOAK_URL
        self.realm = settings.KEYCLOAK_REALM
        self.client_id = settings.KEYCLOAK_ADMIN_CLIENT_ID
        self.client_secret = settings.KEYCLOAK_ADMIN_CLIENT_SECRET

    async def verify_token(self, token: str) -> dict[str, Any]:
        """Verify JWT token and return claims.

        TODO: реализовать в Task 2.
        """
        raise NotImplementedError("KeycloakClient.verify_token not yet implemented — Task 2")

    async def get_user(self, user_id: str) -> dict[str, Any]:
        """Fetch user info from Keycloak.

        TODO: реализовать в Task 5.
        """
        raise NotImplementedError("KeycloakClient.get_user not yet implemented — Task 5")

    async def search_users(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search users in Keycloak.

        TODO: реализовать в Task 5.
        """
        raise NotImplementedError("KeycloakClient.search_users not yet implemented — Task 5")
