"""APScheduler job: sync employees from Keycloak to PostgreSQL cache."""
import logging
from app.clients.keycloak import KeycloakAdminClient
from app.db.database import async_session_maker
from app.db.models import Employee
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)

keycloak_admin = KeycloakAdminClient()


async def sync_employees_from_keycloak() -> int:
    """Fetch all users from Keycloak and upsert into employees table.

    Returns number of employees synced.
    """
    try:
        users = await keycloak_admin.get_all_users()

        if not users:
            logger.warning("Keycloak returned 0 users during sync")
            return 0

        async with async_session_maker() as session:
            for user in users:
                attrs = user.get("attributes", {})

                stmt = insert(Employee).values(
                    id=user["id"],
                    name=f"{user.get('firstName', '')} {user.get('lastName', '')}".strip(),
                    position=_extract_attr(attrs, "position"),
                    department=_extract_attr(attrs, "department"),
                    phone=_extract_attr(attrs, "phone"),
                    email=user.get("email", ""),
                    city=_extract_attr(attrs, "city"),
                    bitrix_id=_extract_attr(attrs, "bitrixId"),
                ).on_conflict_do_update(
                    index_elements=["id"],
                    set_={
                        "name": f"{user.get('firstName', '')} {user.get('lastName', '')}".strip(),
                        "position": _extract_attr(attrs, "position"),
                        "department": _extract_attr(attrs, "department"),
                        "phone": _extract_attr(attrs, "phone"),
                        "email": user.get("email", ""),
                        "city": _extract_attr(attrs, "city"),
                        "bitrix_id": _extract_attr(attrs, "bitrixId"),
                    }
                )
                await session.execute(stmt)

            await session.commit()

        logger.info(f"Employee sync complete: {len(users)} employees synced")
        return len(users)

    except Exception as e:
        logger.error(f"Employee sync failed: {e}")
        raise


def _extract_attr(attributes: dict, key: str) -> str:
    value = attributes.get(key, [])
    if isinstance(value, list):
        return value[0] if value else ""
    return str(value) if value else ""
