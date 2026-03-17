# Bilingual AI Customer Support Voice Agent (Starter)

Production-ready **starter scaffold** for an AI support agent that:
- receives calls (Twilio webhook endpoint);
- can initiate outbound calls (Twilio REST-ready service abstraction);
- answers dynamically (RAG + LLM provider abstraction, no hardcoded fixed script);
- auto-switches between **Romanian** and **English** based on user input each turn.

## 1) Quick start

```bash
cd voice_agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## 2) Run tests

```bash
cd voice_agent
pytest -q
```

## 3) Main endpoints

- `GET /health`
- `POST /api/simulate-turn`  
  JSON: `{ "session_id": "abc", "user_text": "Buna, vreau o factura" }`
- `POST /twilio/voice` (Twilio voice webhook starter)
- `POST /twilio/outbound` (outbound call trigger starter)

## 4) How language switching works

- Language is detected each turn (`ro` / `en`) with confidence.
- Session language is updated continuously.
- Agent response is generated in detected language.
- If user switches language mid-conversation, response follows automatically.

## 5) How to customize for production

### Providers
- Replace `MockLLMProvider` with `OpenAILLMProvider` or your internal model in `app/services/orchestrator.py`.
- Replace Twilio stubs in `app/services/telephony.py` with full call + media streaming pipeline.

### Knowledge base (RAG-lite starter)
- Edit `knowledge/faq.json`.
- Replace `KnowledgeBase.search()` with vector DB retrieval (pgvector/Pinecone/Weaviate).

### CRM / ticketing
- Extend `ToolClient` in `app/services/tools.py`.

## 6) Suggested next step

Add real-time audio streaming (Twilio Media Streams websocket + streaming STT + streaming TTS).
