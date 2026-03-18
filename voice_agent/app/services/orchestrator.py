from typing import Protocol

import httpx

from app.config import settings
from app.services.knowledge_base import KnowledgeMatch


class LLMProvider(Protocol):
    async def generate(
        self,
        user_text: str,
        language: str,
        kb_match: KnowledgeMatch | None,
        context: dict,
        skill_instruction: str | None = None,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> str:
        ...


class MockLLMProvider:
    @staticmethod
    def _already_answered_kb(history: list[dict[str, str]], kb_match: KnowledgeMatch | None) -> bool:
        if not kb_match:
            return False
        recent_assistant_turns = [turn["text"].lower() for turn in history[-4:] if turn["role"] == "assistant"]
        answer_prefix = kb_match.answer.lower()[:30]
        return any(answer_prefix in turn or kb_match.source.lower() in turn for turn in recent_assistant_turns)

    @staticmethod
    def _invoice_follow_up(language: str) -> str:
        if language == "ro":
            return (
                "Pot să te ajut mai concret cu factura. Spune-mi, te rog, dacă vrei retransmiterea pe email, "
                "schimbarea adresei de facturare sau verificarea ultimei plăți."
            )
        return (
            "I can help with the invoice in more detail. Please tell me if you want it resent by email, "
            "need to update the billing address, or want me to check the latest payment."
        )

    async def generate(
        self,
        user_text: str,
        language: str,
        kb_match: KnowledgeMatch | None,
        context: dict,
        skill_instruction: str | None = None,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> str:
        history = conversation_history or []
        skill_text = f" {skill_instruction}" if skill_instruction else ""

        if kb_match and kb_match.confidence >= 0.6:
            repeated = self._already_answered_kb(history, kb_match)
            is_invoice = "factura" in kb_match.source.lower() or "invoice" in kb_match.source.lower()

            if repeated and is_invoice:
                return self._invoice_follow_up(language)

            if language == "ro":
                base = f"Sigur — {kb_match.answer}"
                next_step = (
                    " Dacă vrei, pot continua și să te ghidez mai departe pentru factura ta."
                    if is_invoice
                    else " Dacă vrei, pot continua cu următorul pas."
                )
                return f"{base}{next_step} (Sursă: {kb_match.source})"

            base = f"Sure — {kb_match.answer}"
            next_step = (
                " If you want, I can also guide you through the next invoice step."
                if is_invoice
                else " If you want, I can continue with the next step."
            )
            return f"{base}{next_step} (Source: {kb_match.source})"

        if language == "ro":
            return (
                f"Salut! Sunt {settings.agent_name} de la {settings.business_name}.{skill_text} "
                "Spune-mi pe scurt ce ai nevoie și te ajut pas cu pas."
            )

        return (
            f"Hi! I'm {settings.agent_name} from {settings.business_name}.{skill_text} "
            "Tell me briefly what you need and I'll help step by step."
        )


class OpenAILLMProvider:
    async def generate(
        self,
        user_text: str,
        language: str,
        kb_match: KnowledgeMatch | None,
        context: dict,
        skill_instruction: str | None = None,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> str:
        provider = settings.llm_provider.lower().strip()
        if provider == "groq":
            api_key = settings.groq_api_key
            model = settings.groq_model
            endpoint = settings.groq_base_url
        else:
            api_key = settings.openai_api_key
            model = settings.openai_model
            endpoint = settings.openai_base_url

        if not api_key:
            return await MockLLMProvider().generate(
                user_text,
                language,
                kb_match,
                context,
                skill_instruction,
                conversation_history,
            )

        language_name = "Romanian" if language == "ro" else "English"
        kb_text = kb_match.answer if kb_match else "No KB match found. Ask one concise clarifying question."
        kb_source = kb_match.source if kb_match else "none"
        history = conversation_history or []
        skill_prompt = skill_instruction or "No specific skill active."

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a customer support voice agent in a live phone conversation. "
                        f"Business name: {settings.business_name}. "
                        f"Business domain: {settings.business_domain}. "
                        f"Agent display name: {settings.agent_name}. "
                        "Reply in the same language as the user. "
                        "Keep responses brief, natural, and human-sounding for speech. "
                        "Use knowledge base evidence as grounding, but do not sound like a rigid FAQ bot. "
                        "If the user repeats the same topic, do not repeat the same sentence verbatim; instead move the conversation forward with the next helpful question or action. "
                        "If knowledge base evidence is present, mention the source label naturally. "
                        "If data is missing or confidence is low, ask one clarification question instead of inventing details. "
                        "Recommend a human handoff for billing disputes, legal requests, security concerns, or repeated failures. "
                        f"Behavior EN: {settings.behavior_style_en}. "
                        f"Behavior RO: {settings.behavior_style_ro}."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Language: {language_name}\n"
                        f"Skill instruction: {skill_prompt}\n"
                        f"Customer context: {context}\n"
                        f"Recent conversation turns: {history}\n"
                        f"KB source: {kb_source}\n"
                        f"KB answer: {kb_text}\n"
                        f"User: {user_text}"
                    ),
                },
            ],
            "temperature": 0.6,
        }

        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.post(
                endpoint,
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
            )
            res.raise_for_status()
            body = res.json()

        return body["choices"][0]["message"]["content"].strip()
