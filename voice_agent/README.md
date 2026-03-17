# Bilingual AI Customer Support Voice Agent

Deploy-ready FastAPI service for a customer support voice agent that:
- receives inbound calls (Twilio webhook);
- places outbound calls (Twilio API);
- responds dynamically (knowledge + LLM, not static scripts);
- switches automatically between Romanian and English;
- supports plug-and-play skills (sales/support/retention);
- supports business-specific branding + integrations.

## Features

- **Language auto-switch** (`ro`/`en`) per turn.
- **Business customization** (`BUSINESS_NAME`, `AGENT_NAME`, greetings).
- **Skill router** (`sales`, `support`, `retention`) with easy extension.
- **Knowledge lookup** (`knowledge/faq.json`) for grounded answers.
- **DB integration ready** with a default **SQLite** implementation that works out-of-the-box.
- **CRM API connector** for external software.
- **Twilio inbound/outbound endpoints**.
- **Docker deployment** included.

---

## 1) Local run

```bash
cd voice_agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

---

## 2) Deploy with Docker

```bash
cd voice_agent
docker build -t voice-agent .
docker run -p 8000:8000 --env-file .env voice-agent
```

If you deploy to Render, a basic `render.yaml` is included.

---

## 3) Required environment variables

Copy `.env.example` and set values:

- App/runtime:
  - `APP_NAME`, `ENVIRONMENT`, `HOST`, `PORT`, `PUBLIC_BASE_URL`
- Business:
  - `BUSINESS_NAME`, `BUSINESS_DOMAIN`, `AGENT_NAME`, `GREETING_RO`, `GREETING_EN`
- LLM:
  - `OPENAI_API_KEY`, `OPENAI_MODEL`
- Twilio:
  - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`
- Integrations:
  - `DATABASE_URL` (defaults to SQLite)
  - `CRM_API_BASE_URL`, `CRM_API_KEY`

---

## 4) API endpoints

- `GET /health`
- `GET /api/skills`
- `POST /api/simulate-turn`
- `POST /twilio/voice`
- `POST /twilio/outbound`

Example simulate turn:

```bash
curl -X POST http://localhost:8000/api/simulate-turn \
  -H "Content-Type: application/json" \
  -d '{"session_id":"abc","user_text":"Buna, vreau factura"}'
```

---

## 5) Twilio setup

1. Deploy this service publicly (HTTPS).
2. In Twilio Phone Number Voice webhook, set URL to:
   - `https://your-domain.com/twilio/voice`
3. Set method `POST`.
4. Fill Twilio credentials in `.env` for outbound calls.

---

## 6) Plug-and-play skills

Defined in `app/services/agent_skills.py`:
- `sales`
- `support`
- `retention`

To add a new skill:
1. Add class with `can_handle()` + `prompt_instruction()`.
2. Register in `SkillRegistry`.
3. Add tests.

---

## 7) Database + client software integration

- `DatabaseClient` uses SQLite by default (`voice_agent.db`) so deployment works immediately.
- `CRMClient` integrates external software APIs (HubSpot/Salesforce/Zoho/custom).
- `ToolClient` merges DB + CRM context and passes it to the LLM.

For enterprise rollout, replace SQLite implementation with your production DB driver and schema.

---

## 8) Tests

```bash
cd voice_agent
pytest -q
```

If dependencies are unavailable in your environment, run at least syntax validation:

```bash
python -m compileall app
```
