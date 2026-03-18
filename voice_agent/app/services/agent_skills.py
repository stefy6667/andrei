from dataclasses import dataclass
from typing import Protocol


@dataclass
class SkillContext:
    language: str
    user_text: str


class AgentSkill(Protocol):
    name: str
    description: str

    def can_handle(self, ctx: SkillContext) -> bool:
        ...

    def prompt_instruction(self, language: str) -> str:
        ...


class SalesSkill:
    name = "sales"
    description = "Handles pricing, offers, upgrades, and new purchase intent."

    RO_KEYWORDS = {"pret", "preț", "oferta", "ofertă", "cumpar", "cumpăr", "abonament", "upgrade"}
    EN_KEYWORDS = {"price", "pricing", "offer", "buy", "purchase", "subscription", "upgrade"}

    def can_handle(self, ctx: SkillContext) -> bool:
        text = ctx.user_text.lower()
        keywords = self.RO_KEYWORDS if ctx.language == "ro" else self.EN_KEYWORDS
        return any(word in text for word in keywords)

    def prompt_instruction(self, language: str) -> str:
        if language == "ro":
            return "Skill activ: SALES. Identifică nevoia clientului, recomandă opțiuni clare, apoi cere acordul pentru următorul pas comercial."
        return "Active skill: SALES. Identify needs, propose clear options, and ask for consent for the next commercial step."


class SupportSkill:
    name = "support"
    description = "Handles incidents, troubleshooting, and technical/account issues."

    RO_KEYWORDS = {"problema", "problemă", "nu merge", "eroare", "cont", "resetare"}
    EN_KEYWORDS = {"issue", "problem", "not working", "error", "account", "reset"}

    def can_handle(self, ctx: SkillContext) -> bool:
        text = ctx.user_text.lower()
        keywords = self.RO_KEYWORDS if ctx.language == "ro" else self.EN_KEYWORDS
        return any(word in text for word in keywords)

    def prompt_instruction(self, language: str) -> str:
        if language == "ro":
            return "Skill activ: SUPPORT. Pune întrebări de diagnostic și oferă pași simpli, verificabili."
        return "Active skill: SUPPORT. Ask diagnostic questions and provide simple, verifiable steps."


class RetentionSkill:
    name = "retention"
    description = "Handles cancellation/churn risk and retention offers."

    RO_KEYWORDS = {"anulare", "anulez", "renunt", "renunț", "inchid", "închid"}
    EN_KEYWORDS = {"cancel", "close account", "terminate", "leave", "churn"}

    def can_handle(self, ctx: SkillContext) -> bool:
        text = ctx.user_text.lower()
        keywords = self.RO_KEYWORDS if ctx.language == "ro" else self.EN_KEYWORDS
        return any(word in text for word in keywords)

    def prompt_instruction(self, language: str) -> str:
        if language == "ro":
            return "Skill activ: RETENTION. Înțelege motivul plecării, oferă alternative relevante și evită presiunea."
        return "Active skill: RETENTION. Understand churn reason, offer relevant alternatives, and avoid pressure."


class SchedulingSkill:
    name = "scheduling"
    description = "Handles meeting booking, calendar coordination, and callback scheduling."

    RO_KEYWORDS = {"programare", "programeaza", "programează", "intalnire", "întâlnire", "apel", "calendar"}
    EN_KEYWORDS = {"schedule", "meeting", "meet", "callback", "calendar", "book a call"}

    def can_handle(self, ctx: SkillContext) -> bool:
        text = ctx.user_text.lower()
        keywords = self.RO_KEYWORDS if ctx.language == "ro" else self.EN_KEYWORDS
        return any(word in text for word in keywords)

    def prompt_instruction(self, language: str) -> str:
        if language == "ro":
            return "Skill activ: SCHEDULING. Colectează datele necesare pentru programare și propune următorul pas pentru creare calendar/Google Meet."
        return "Active skill: SCHEDULING. Collect the details needed to schedule a meeting and propose the next step for calendar/Google Meet creation."


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: list[AgentSkill] = [SalesSkill(), SupportSkill(), RetentionSkill(), SchedulingSkill()]

    def list_skills(self) -> list[dict[str, str]]:
        return [{"name": s.name, "description": s.description} for s in self._skills]

    def resolve(self, language: str, user_text: str) -> AgentSkill | None:
        ctx = SkillContext(language=language, user_text=user_text)
        for skill in self._skills:
            if skill.can_handle(ctx):
                return skill
        return None
