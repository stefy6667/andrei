from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "voice-agent"
    environment: str = "production"
    host: str = "0.0.0.0"
    port: int = 8000
    public_base_url: str = "http://localhost:8000"

    # Business customization
    business_name: str = "Your Company"
    business_domain: str = "general support"
    agent_name: str = "Alex"
    greeting_ro: str = "Bună! Sunt {agent_name} de la {business_name}. Cu ce te pot ajuta astăzi?"
    greeting_en: str = "Hello! I'm {agent_name} from {business_name}. How can I help you today?"
    intro_only_mode: bool = False

    # LLM config
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Telephony
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_from_number: str = ""
    twilio_voice_en: str = "Polly.Amy-Neural"
    twilio_voice_ro: str = "Polly.Carmen"

    # Conversation behavior
    behavior_style_en: str = "Warm, friendly, concise, and natural. Use short sentences and empathy."
    behavior_style_ro: str = "Cald, prietenos, concis și natural. Folosește propoziții scurte și empatie."

    # Data integrations
    database_url: str = "sqlite:///./voice_agent.db"
    crm_api_base_url: str = ""
    crm_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
