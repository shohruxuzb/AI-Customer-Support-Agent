from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[Message] = []
    provider: str = "openai"  # "openai" or "groq"
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
