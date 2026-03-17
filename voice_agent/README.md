# Bilingual AI Customer Support Voice Agent (Starter)

Production-ready **starter scaffold** for an AI support agent that:
- receives calls (Twilio webhook endpoint);
- can initiate outbound calls (Twilio REST-ready service abstraction);
- answers dynamically (RAG + LLM provider abstraction, no hardcoded fixed script);
- auto-switches between **Romanian** and **English** based on user input each turn;
- can be customized per client business (company name, domain, agent identity, greetings);
- can connect with client database + CRM/software APIs;
- supports plug-and-play business skills (Sales, Support, Retention) and easy extension.

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
- `GET /api/skills` (list installed plug-and-play skills)
- `POST /api/simulate-turn`  
  JSON: `{ "session_id": "abc", "user_text": "Buna, vreau o factura" }`
- `POST /twilio/voice` (Twilio voice webhook starter)
- `POST /twilio/outbound` (outbound call trigger starter)

## 4) Plug-and-play skills

Implemented in `app/services/agent_skills.py`:
- `sales`
- `support`
- `retention`

How it works:
- The app auto-detects an appropriate skill per turn from user intent.
- The selected skill injects focused instructions into the LLM prompt.
- If no skill matches, it falls back to generic assistant behavior.

To add a new skill (e.g., billing/collections/appointments):
1. Create a new class implementing `can_handle()` and `prompt_instruction()`.
2. Register it in `SkillRegistry`.
3. (Optional) add tests for selection behavior.

## 5) Business customization

Set in `.env`:
- `BUSINESS_NAME`
- `BUSINESS_DOMAIN`
- `AGENT_NAME`
- `GREETING_RO`
- `GREETING_EN`

These are injected into greetings and LLM system instructions.

## 6) Database + client software integration

- `app/services/integrations.py` contains:
  - `DatabaseClient` (placeholder adapter for PostgreSQL/MySQL/etc)
  - `CRMClient` (generic API adapter for HubSpot/Salesforce/Zoho/custom ERP/CRM)
- `ToolClient` combines these to build runtime customer context for the LLM.
- Configure with `.env`:
  - `DATABASE_URL`
  - `CRM_API_BASE_URL`
  - `CRM_API_KEY`

## 7) How language switching works

- Language is detected each turn (`ro` / `en`) with confidence.
- Session language is updated continuously.
- Agent response is generated in detected language.
- If user switches language mid-conversation, response follows automatically.

## 8) How to customize for production

### Providers
- Replace `OpenAILLMProvider` with your preferred model/provider if needed.
- Replace Twilio stubs in `app/services/telephony.py` with full call + media streaming pipeline.

### Knowledge base (RAG-lite starter)
- Edit `knowledge/faq.json`.
- Replace `KnowledgeBase.search()` with vector DB retrieval (pgvector/Pinecone/Weaviate).

### Business software
- Extend `DatabaseClient.fetch_customer_profile()` with real queries.
- Extend `CRMClient.fetch_open_tickets()` and add additional methods (orders, invoices, subscriptions).

## 9) Suggested next step

Add real-time audio streaming (Twilio Media Streams websocket + streaming STT + streaming TTS).
