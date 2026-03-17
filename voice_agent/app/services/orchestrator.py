from typing import Protocol

import httpx

from app.config import settings


class LLMProvider(Protocol):
    async def generate(self, user_text: str, language: str, kb_answer: str | None, context: dict) -> str:
        ...


class MockLLMProvider:
    async def generate(self, user_text: str, language: str, kb_answer: str | None, context: dict) -> str:
        if kb_answer:
            return kb_answer

        if language == "ro":
            return (
                f"Sunt {settings.agent_name} de la {settings.business_name}. "
                "Te pot ajuta cu această solicitare. Îmi poți da mai multe detalii "
                "ca să verific corect în sistem?"
            )

        return (
            f"I'm {settings.agent_name} from {settings.business_name}. "
            "I can help with this request. Could you share a few more details so I can verify properly?"
        )


class OpenAILLMProvider:
    async def generate(self, user_text: str, language: str, kb_answer: str | None, context: dict) -> str:
        if not settings.openai_api_key:
            return await MockLLMProvider().generate(user_text, language, kb_answer, context)

        language_name = "Romanian" if language == "ro" else "English"
        context_text = kb_answer or "No KB match found. Ask concise clarification question."

        payload = {
            "model": settings.openai_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a customer support voice agent. "
                        f"Business name: {settings.business_name}. "
                        f"Business domain: {settings.business_domain}. "
                        f"Agent display name: {settings.agent_name}. "
                        "Reply in the same language as the user. "
                        "Do not invent policy details. "
                        "Use available customer context and be concise."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Language: {language_name}\n"
                        f"Customer context: {context}\n"
                        f"KB: {context_text}\n"
                        f"User: {user_text}"
                    ),
                },
            ],
            "temperature": 0.3,
        }

        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.openai_api_key}"},
                json=payload,
            )
            res.raise_for_status()
            body = res.json()

        return body["choices"][0]["message"]["content"].strip()
