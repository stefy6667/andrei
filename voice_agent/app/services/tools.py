from app.services.calendar import CalendarClient
from app.services.integrations import CRMClient, DatabaseClient
from app.services.telephony import TelephonyService


class ToolClient:
    def __init__(
        self,
        db: DatabaseClient,
        crm: CRMClient,
        telephony: TelephonyService,
        calendar: CalendarClient,
    ) -> None:
        self.db = db
        self.crm = crm
        self.telephony = telephony
        self.calendar = calendar

    async def get_customer_context(self, session_id: str) -> dict:
        profile = await self.db.fetch_customer_profile(session_id)
        tickets = await self.crm.fetch_open_tickets(profile.get("customer_id"))

        return {
            "session_id": session_id,
            "customer_id": profile.get("customer_id"),
            "tier": profile.get("tier", "standard"),
            "open_tickets": tickets.get("open_tickets", 0),
            "database_connected": profile.get("database_connected", False),
            "crm_connected": tickets.get("crm_connected", False),
            "calendar_connected": self.calendar.configured(),
        }

    async def schedule_meeting(
        self,
        attendee_email: str,
        start_iso: str,
        end_iso: str,
        summary: str,
        description: str,
    ) -> dict:
        return await self.calendar.schedule_meeting(attendee_email, start_iso, end_iso, summary, description)

    async def send_sms(self, to_number: str, message: str) -> dict:
        return await self.telephony.send_sms(to_number, message)
