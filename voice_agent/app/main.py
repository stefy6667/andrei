from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.models import SimulateTurnRequest, SimulateTurnResponse, TwilioOutboundRequest
from app.services.integrations import build_integration_clients
from app.services.knowledge_base import KnowledgeBase
from app.services.language import LanguageDetector
from app.services.orchestrator import OpenAILLMProvider
from app.services.session_store import SessionStore
from app.services.telephony import TelephonyService
from app.services.tools import ToolClient

app = FastAPI(title="Bilingual Voice Agent")

language_detector = LanguageDetector()
kb = KnowledgeBase()
llm = OpenAILLMProvider()
sessions = SessionStore()
db_client, crm_client = build_integration_clients()
tools = ToolClient(db_client, crm_client)
telephony = TelephonyService()


def build_intro(language: str) -> str:
    template = settings.greeting_ro if language == "ro" else settings.greeting_en
    return template.format(agent_name=settings.agent_name, business_name=settings.business_name)


@app.get("/health")
async def health() -> dict:
    return {"ok": True, "business": settings.business_name}


@app.post("/api/simulate-turn", response_model=SimulateTurnResponse)
async def simulate_turn(payload: SimulateTurnRequest) -> SimulateTurnResponse:
    detection = language_detector.detect(payload.user_text)
    sessions.upsert_language(payload.session_id, detection.language)

    context = await tools.get_customer_context(payload.session_id)
    kb_answer = kb.search(payload.user_text, detection.language)
    answer = await llm.generate(payload.user_text, detection.language, kb_answer, context)

    source = "knowledge_base" if kb_answer else "llm"
    return SimulateTurnResponse(
        session_id=payload.session_id,
        language=detection.language,
        answer=answer,
        source=source,
    )


@app.post("/twilio/voice", response_class=PlainTextResponse)
async def twilio_voice(
    CallSid: str = Form(default=""),
    SpeechResult: str = Form(default=""),
) -> str:
    session_id = CallSid or "unknown-call"

    if not SpeechResult:
        intro = build_intro("en")
        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<Response><Say language="en-US">{intro}</Say><Gather input="speech" /></Response>'
        )

    detection = language_detector.detect(SpeechResult)
    sessions.upsert_language(session_id, detection.language)

    context = await tools.get_customer_context(session_id)
    kb_answer = kb.search(SpeechResult, detection.language)
    answer = await llm.generate(SpeechResult, detection.language, kb_answer, context)

    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f"<Response><Say language=\"{'ro-RO' if detection.language == 'ro' else 'en-US'}\">"
        f"{answer}</Say></Response>"
    )


@app.post("/twilio/outbound")
async def outbound_call(payload: TwilioOutboundRequest) -> dict:
    return await telephony.create_outbound_call(payload.to_number, payload.message, payload.language)
