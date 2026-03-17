from app.config import settings


class TelephonyService:
    async def create_outbound_call(self, to_number: str, message: str, language: str) -> dict:
        intro = (settings.greeting_ro if language == "ro" else settings.greeting_en).format(
            agent_name=settings.agent_name,
            business_name=settings.business_name,
        )
        # Replace this stub with Twilio REST API call in production.
        return {
            "provider": "twilio_stub",
            "account_configured": bool(settings.twilio_account_sid and settings.twilio_auth_token),
            "to": to_number,
            "language": language,
            "business": settings.business_name,
            "preview_message": f"{intro} {message}",
            "status": "queued_stub",
        }
