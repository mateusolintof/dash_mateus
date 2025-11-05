from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class ChatMessage(BaseModel):
    role: str  # 'user' ou 'assistant'
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    message: str
    timestamp: datetime


class AIChatHistoryResponse(BaseModel):
    id: UUID
    message: str
    response: str
    model: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
