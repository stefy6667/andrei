class ToolClient:
    async def get_customer_context(self, session_id: str) -> dict:
        return {
            "session_id": session_id,
            "tier": "standard",
            "open_tickets": 0,
        }
