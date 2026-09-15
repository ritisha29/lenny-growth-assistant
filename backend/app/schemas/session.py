from datetime import datetime

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    title: str | None = Field(
        default=None,
        max_length=255,
    )


class SessionResponse(BaseModel):
    id: str
    title: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }