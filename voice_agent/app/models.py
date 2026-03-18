from pydantic import BaseModel, Field


class SimulateTurnRequest(BaseModel):
    session_id: str = Field(min_length=1)
    user_text: str = Field(min_length=1)


class SimulateTurnResponse(BaseModel):
    session_id: str
    language: str
    answer: str
    source: str
    skill: str | None = None
    handoff_recommended: bool = False
    citations: list[str] = Field(default_factory=list)


class TwilioOutboundRequest(BaseModel):
    to_number: str = Field(min_length=5)
    message: str = Field(min_length=1)
    language: str = Field(default="en")
