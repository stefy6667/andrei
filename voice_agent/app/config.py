from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "voice-agent"

    # Business customization
    business_name: str = "Your Company"
    business_domain: str = "general support"
    agent_name: str = "Alex"
    greeting_ro: str = "Bună! Sunt {agent_name} de la {business_name}. Cu ce te pot ajuta astăzi?"
    greeting_en: str = "Hello! I'm {agent_name} from {business_name}. How can I help you today?"

    # LLM config
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Telephony
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_from_number: str = ""

    # Data integrations
    database_url: str = ""
    crm_api_base_url: str = ""
    crm_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
