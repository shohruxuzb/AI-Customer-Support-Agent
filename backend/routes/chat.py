from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from backend.services.shared import vector_store, llm_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Retrieve relevant chunks
        context = vector_store.search(request.message, top_k=3)
        
        # 2. Get AI response
        response = await llm_service.get_response(
            query=request.message,
            context=context,
            chat_history=request.history
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
