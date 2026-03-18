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
    async def generate(
        self,
        user_text: str,
        language: str,
        kb_match: KnowledgeMatch | None,
        context: dict,
        skill_instruction: str | None = None,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> str:
        if kb_match and kb_match.confidence >= 0.6:
            return (
                f"{kb_match.answer} (Sursă: {kb_match.source})"
                if language == "ro"
                else f"{kb_match.answer} (Source: {kb_match.source})"
            )

        skill_text = f" [{skill_instruction}]" if skill_instruction else ""
        if language == "ro":
            return (
                f"Salut! Sunt {settings.agent_name} de la {settings.business_name}.{skill_text} "
                "Te pot ajuta, dar am nevoie de încă un detaliu ca să răspund corect."
            )

        return (
            f"Hi! I'm {settings.agent_name} from {settings.business_name}.{skill_text} "
            "I can help, but I need one more detail so I can answer accurately."
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
                        "Keep responses brief and natural for speech. "
                        "If knowledge base evidence is present, use it and cite the source label in the response. "
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
            "temperature": 0.45,
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
