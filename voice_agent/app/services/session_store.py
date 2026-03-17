class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, str]] = {}

    def upsert_language(self, session_id: str, language: str) -> None:
        self._sessions.setdefault(session_id, {})["language"] = language

    def get_language(self, session_id: str) -> str | None:
        session = self._sessions.get(session_id, {})
        return session.get("language")
