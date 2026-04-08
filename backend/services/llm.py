import os
from groq import AsyncGroq
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class LLMService:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = AsyncGroq(api_key=self.api_key)
        self.model_name = model_name

    async def get_response(self, query: str, context: List[str], chat_history: List[Dict[str, str]]) -> str:
        # Build context string
        context_str = "\n\n".join(context)
        
        # System prompt for Customer Support Persona
        system_prompt = (
            "You are a helpful and professional customer support agent for a business. "
            "Use the provided context to answer the user's questions. "
            "If the answer is not in the context, politely inform the user that you don't have that information. "
            "Keep your responses concise and friendly."
        )
        
        # Construct messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history (last few messages)
        for msg in chat_history[-5:]: # Keep last 5 messages for memory
            messages.append(msg)
            
        # Add user query with context
        user_content = f"Context:\n{context_str}\n\nUser Question: {query}"
        messages.append({"role": "user", "content": user_content})

        try:
            completion = await self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=0.7,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
