from __future__ import annotations

from typing import Any

import httpx

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


class KeycloakAdminClient:
    """Keycloak Admin API client for employee sync (used by APScheduler)."""

    def __init__(self) -> None:
        self.base_url = settings.KEYCLOAK_URL
        self.realm = settings.KEYCLOAK_REALM
        self.client_id = settings.KEYCLOAK_ADMIN_CLIENT_ID
        self.client_secret = settings.KEYCLOAK_ADMIN_CLIENT_SECRET
        self._access_token: str | None = None

    async def _get_token(self) -> str:
        """Get admin access token via client_credentials grant."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/realms/master/protocol/openid-connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            response.raise_for_status()
            return response.json()["access_token"]

    async def get_all_users(self, max_count: int = 2000) -> list[dict[str, Any]]:
        """Fetch all realm users for employee sync."""
        token = await self._get_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/admin/realms/{self.realm}/users",
                headers={"Authorization": f"Bearer {token}"},
                params={"max": max_count, "enabled": "true"},
            )
            response.raise_for_status()
            return response.json()
