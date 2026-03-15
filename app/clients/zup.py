from __future__ import annotations

from typing import Any

import httpx

from app.config import settings


class ZUPClient:
    """1С ЗУП (Zarplata i Upravleniye Personalom) web service client.

    Used for HR data: vacations, sick days, salary info, etc.
    TODO: реализовать полностью.
    """

    def __init__(self) -> None:
        self.webservice_url = settings.ZUP_WEBSERVICE_URL
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> ZUPClient:
        self._client = httpx.AsyncClient(timeout=60.0)
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def get_vacation_balance(self, employee_id: str) -> dict[str, Any]:
        """Get vacation balance for an employee.

        TODO: реализовать.
        """
        raise NotImplementedError("ZUPClient.get_vacation_balance not yet implemented")

    async def get_hr_info(self, employee_id: str, topic: str) -> dict[str, Any]:
        """Get HR information for an employee by topic.

        TODO: реализовать.
        """
        raise NotImplementedError("ZUPClient.get_hr_info not yet implemented")
