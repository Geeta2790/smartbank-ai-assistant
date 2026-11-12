
from pydantic import BaseModel, Field
from datetime import datetime


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    session_id: int | None = Field(default=None, gt=0)


class ChatResponse(BaseModel):
    session_id: int
    intent: str
    answer: str


class SessionResponse(BaseModel):
    session_id: int
    created_at: datetime


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str


class HistoryResponse(BaseModel):
    session_id: int
    messages: list[MessageResponse]
