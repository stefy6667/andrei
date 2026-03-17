from app.config import settings


class TelephonyService:
    async def create_outbound_call(self, to_number: str, message: str, language: str) -> dict:
        # Replace this stub with Twilio REST API call in production.
        return {
            "provider": "twilio_stub",
            "account_configured": bool(settings.twilio_account_sid and settings.twilio_auth_token),
            "to": to_number,
            "language": language,
            "preview_message": message,
            "status": "queued_stub",
        }
