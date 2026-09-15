from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(min_length=1, max_length=10000)


class Source(BaseModel):
    episode_title: str
    guest: str | None = None
    date: str | None = None
    source_url: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]