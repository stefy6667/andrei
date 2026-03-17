# AI Customer Support Voice Agent (Romanian + English)

## Goal
Build an AI voice agent that can:
- receive inbound calls;
- make outbound calls;
- understand caller intent in real time;
- answer dynamically (not hardcoded);
- switch automatically between Romanian and English depending on the caller language.

## Recommended Architecture

1. **Telephony Layer**
   - Twilio Voice, Vonage, or Plivo for inbound/outbound calls.
   - SIP trunk if you already have a PBX/CRM phone system.

2. **Real-Time Speech Pipeline**
   - **Streaming STT (speech-to-text)** with strong Romanian + English support (e.g., Deepgram, Google STT, Azure Speech).
   - **LLM Orchestrator** for reasoning and response generation (GPT family).
   - **TTS (text-to-speech)** with natural bilingual voices (Azure Neural voices / ElevenLabs multilingual voices).

3. **Knowledge + Business Tools (No Hardcoded Responses)**
   - RAG (Retrieval-Augmented Generation) over your docs: FAQ, policy, pricing, contracts.
   - Tool calls to CRM, order system, ticketing, calendar.
   - Dynamic response policy:
     - if answer exists in knowledge base → answer with citation/source;
     - if missing/confidence low → ask clarification or escalate to human.

4. **Language Detection + Auto-Switch**
   - Detect language on each caller turn (or every few seconds).
   - Track active language in session state (`ro` / `en`).
   - Generate and synthesize response in detected language.
   - If the caller switches language mid-call, agent switches immediately.

5. **Conversation State + Guardrails**
   - Session memory: caller profile, previous turns, open issue.
   - Safety and compliance rules (PII masking, forbidden actions).
   - Fallback routing to human agent when needed.

## Core Call Flow

1. Incoming call received by telephony provider.
2. Audio stream sent to your voice gateway/websocket service.
3. STT converts speech to text in near real time.
4. Language detector updates current language (`ro`/`en`).
5. Orchestrator builds prompt using:
   - system policy,
   - conversation history,
   - retrieved knowledge,
   - tool outputs (CRM/tickets/orders).
6. LLM generates response in caller language.
7. TTS speaks response back on call.
8. Log transcript + events + quality metrics.
9. If unresolved/high-risk → transfer to human.

## Prompting Strategy (Important)

Use a strict system prompt so the model:
- never uses hardcoded canned answers as the only source;
- always prefers knowledge base + tool data;
- speaks naturally and briefly;
- mirrors caller language.

Example policy snippet:

- "Detect caller language every turn. Reply in the same language (Romanian or English)."
- "If confidence < threshold or missing data, ask a clarification question before answering."
- "Do not invent policy details. If unknown, say you will transfer to a human agent."

## Romanian + English Voice Quality Tips

- Pick one premium TTS voice for Romanian and one for English.
- Normalize numbers/dates before TTS (for natural pronunciation).
- Add pronunciation dictionaries for brand names.
- Keep latency under ~900 ms turn-to-turn for natural calls.

## Minimum Production Features

- Inbound + outbound calling
- Real-time transcription
- Automatic language switching (RO/EN)
- RAG over company knowledge
- CRM integration
- Human handoff
- Call recordings and transcripts
- Analytics dashboard (AHT, containment rate, CSAT)

## Suggested MVP Roadmap (4 weeks)

### Week 1
- Telephony integration + call streaming.
- Basic STT/TTS loop.

### Week 2
- LLM orchestrator + bilingual language switching.
- Session memory.

### Week 3
- RAG + CRM/ticketing tools.
- Handoff workflow.

### Week 4
- QA testing with real call scripts in RO/EN.
- Monitoring, guardrails, and launch.

## KPIs to Track

- First Call Resolution (FCR)
- Containment rate (AI-only solved calls)
- Average Handle Time (AHT)
- Escalation rate to human
- Language switch accuracy
- Customer Satisfaction (CSAT)

## Quick Stack Recommendation

- **Telephony:** Twilio Voice
- **STT:** Deepgram or Azure Speech
- **LLM:** GPT model with tool calling
- **TTS:** Azure Neural or ElevenLabs
- **Backend:** Python (FastAPI) or Node.js
- **Vector DB:** pgvector / Pinecone / Weaviate
- **Observability:** OpenTelemetry + Grafana

## Next Step

If you want, the next step is to build a concrete implementation skeleton:
- FastAPI service,
- Twilio webhook endpoints,
- websocket audio pipeline,
- language switch middleware,
- RAG retrieval endpoint,
- and CRM tool adapters.
