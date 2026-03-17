from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.models import SimulateTurnRequest, SimulateTurnResponse, TwilioOutboundRequest
from app.services.agent_skills import SkillRegistry
from app.services.integrations import build_integration_clients
from app.services.knowledge_base import KnowledgeBase
from app.services.language import LanguageDetector
from app.services.orchestrator import OpenAILLMProvider
from app.services.session_store import SessionStore
from app.services.telephony import TelephonyService
from app.services.tools import ToolClient

app = FastAPI(title="Bilingual Voice Agent")

language_detector = LanguageDetector()
skill_registry = SkillRegistry()
kb = KnowledgeBase()
llm = OpenAILLMProvider()
sessions = SessionStore()
db_client, crm_client = build_integration_clients()
tools = ToolClient(db_client, crm_client)
telephony = TelephonyService()


def build_intro(language: str) -> str:
    template = settings.greeting_ro if language == "ro" else settings.greeting_en
    return template.format(agent_name=settings.agent_name, business_name=settings.business_name)


def twilio_voice_for_language(language: str) -> str:
    return settings.twilio_voice_ro if language == "ro" else settings.twilio_voice_en


def gather_loop() -> str:
    return (
        "<Gather input=\"speech\" action=\"/twilio/voice\" method=\"POST\" timeout=\"5\" speechTimeout=\"auto\" />"
        "<Pause length=\"1\"/>"
        "<Redirect method=\"POST\">/twilio/voice</Redirect>"
    )


def intro_only_response(language: str, session_id: str) -> SimulateTurnResponse:
    intro = build_intro(language)
    sessions.upsert_language(session_id, language)
    return SimulateTurnResponse(
        session_id=session_id,
        language=language,
        answer=intro,
        source="intro_only",
        skill=None,
    )


@app.get("/health")
async def health() -> dict:
    return {
        "ok": True,
        "app": settings.app_name,
        "environment": settings.environment,
        "business": settings.business_name,
        "skills": len(skill_registry.list_skills()),
    }


@app.get("/api/skills")
async def list_skills() -> dict:
    return {"skills": skill_registry.list_skills()}


@app.post("/api/simulate-turn", response_model=SimulateTurnResponse)
async def simulate_turn(payload: SimulateTurnRequest) -> SimulateTurnResponse:
    detection = language_detector.detect(payload.user_text)

    if settings.intro_only_mode:
        return intro_only_response(detection.language, payload.session_id)

    sessions.upsert_language(payload.session_id, detection.language)

    context = await tools.get_customer_context(payload.session_id)
    kb_answer = kb.search(payload.user_text, detection.language)
    active_skill = skill_registry.resolve(detection.language, payload.user_text)
    skill_instruction = active_skill.prompt_instruction(detection.language) if active_skill else None
    answer = await llm.generate(payload.user_text, detection.language, kb_answer, context, skill_instruction)

    source = "knowledge_base" if kb_answer else "llm"
    return SimulateTurnResponse(
        session_id=payload.session_id,
        language=detection.language,
        answer=answer,
        source=source,
        skill=active_skill.name if active_skill else None,
    )


@app.post("/twilio/voice", response_class=PlainTextResponse)
async def twilio_voice(
    CallSid: str = Form(default=""),
    SpeechResult: str = Form(default=""),
) -> str:
    session_id = CallSid or "unknown-call"

    if not SpeechResult:
        intro = f"{build_intro('en')} / {build_intro('ro')}"
        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<Response><Say voice="{settings.twilio_voice_en}" language="en-US">{intro}</Say>'
            f"{gather_loop()}"
            "</Response>"
        )

    detection = language_detector.detect(SpeechResult)

    if settings.intro_only_mode:
        intro = build_intro(detection.language)
        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f"<Response><Say voice=\"{twilio_voice_for_language(detection.language)}\" language=\"{'ro-RO' if detection.language == 'ro' else 'en-US'}\">"
            f"{intro}</Say>"
            f"{gather_loop()}"
            "</Response>"
        )

    sessions.upsert_language(session_id, detection.language)

    context = await tools.get_customer_context(session_id)
    kb_answer = kb.search(SpeechResult, detection.language)
    active_skill = skill_registry.resolve(detection.language, SpeechResult)
    skill_instruction = active_skill.prompt_instruction(detection.language) if active_skill else None
    answer = await llm.generate(SpeechResult, detection.language, kb_answer, context, skill_instruction)

    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f"<Response><Say voice=\"{twilio_voice_for_language(detection.language)}\" language=\"{'ro-RO' if detection.language == 'ro' else 'en-US'}\">"
        f"{answer}</Say>"
        f"{gather_loop()}"
        "</Response>"
    )


@app.post("/twilio/outbound")
async def outbound_call(payload: TwilioOutboundRequest) -> dict:
    return await telephony.create_outbound_call(payload.to_number, payload.message, payload.language)
