from typing import Any

import httpx

from app.config import settings


class DatabaseClient:
    """
    Minimal DB adapter placeholder.
    Replace internals with SQLAlchemy/asyncpg for production queries.
    """

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    async def fetch_customer_profile(self, session_id: str) -> dict[str, Any]:
        # Stub for now; real devs can map session_id -> customer_id and query DB.
        return {
            "session_id": session_id,
            "customer_id": None,
            "database_connected": bool(self.database_url),
        }


class CRMClient:
    """
    Generic CRM software connector.
    Can be reused for HubSpot, Salesforce, Zoho, custom ERP/CRM APIs.
    """

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    async def fetch_open_tickets(self, customer_id: str | None) -> dict[str, Any]:
        if not self.base_url or not self.api_key or not customer_id:
            return {
                "crm_connected": bool(self.base_url and self.api_key),
                "open_tickets": 0,
            }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.base_url}/customers/{customer_id}/tickets",
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            data = response.json()

        return {
            "crm_connected": True,
            "open_tickets": len(data.get("tickets", [])),
        }


def build_integration_clients() -> tuple[DatabaseClient, CRMClient]:
    return (
        DatabaseClient(settings.database_url),
        CRMClient(settings.crm_api_base_url, settings.crm_api_key),
    )
