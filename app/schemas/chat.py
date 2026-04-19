from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Класс схемы запроса к чату с LLM."""
    prompt: str = Field(..., min_length=1)
    system: Optional[str] = None
    max_history: int = Field(12, ge=1, le=50)
    temperature: float = Field(0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    """Класс схемы ответа от чата."""
    answer: str