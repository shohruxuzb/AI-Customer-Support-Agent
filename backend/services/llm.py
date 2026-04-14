import os
from openai import OpenAI
from groq import Groq
from typing import List

class LLMProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def generate_response(self, query: str, context: List[str], history: List) -> str:
        raise NotImplementedError

class OpenAILLM(LLMProvider):
    def generate_response(self, query: str, context: List[str], history: List) -> str:
        if not self.api_key:
            return "Error: OpenAI API Key is missing. Please provide it in the sidebar."
        
        try:
            client = OpenAI(api_key=self.api_key)
            system_prompt = self._build_system_prompt(context)
            
            messages = [{"role": "system", "content": system_prompt}]
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})
            messages.append({"role": "user", "content": query})
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"

    def _build_system_prompt(self, context: List[str]) -> str:
        prompt = (
            "You are a helpful AI Customer Support Assistant.\n"
            "Use the provided context to answer the user's query.\n"
            "If the answer is not in the context, politely say 'I don't have enough information to answer that based on the provided documents.'\n\n"
        )
        if context:
            prompt += "Context:\n" + "\n---\n".join(context)
        else:
            prompt += "Context:\nNo documents have been uploaded yet."
        return prompt


class GroqLLM(LLMProvider):
    def generate_response(self, query: str, context: List[str], history: List) -> str:
        if not self.api_key:
            return "Error: Groq API Key is missing. Please provide it in the sidebar."
        
        try:
            client = Groq(api_key=self.api_key)
            system_prompt = self._build_system_prompt(context)
            
            messages = [{"role": "system", "content": system_prompt}]
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})
            messages.append({"role": "user", "content": query})
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Fast and reliable Groq model
                messages=messages,
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq API Error: {str(e)}"

    def _build_system_prompt(self, context: List[str]) -> str:
        prompt = (
            "You are a helpful AI Customer Support Assistant.\n"
            "Use the provided context to answer the user's query.\n"
            "If the answer is not in the context, politely say 'I don't have enough information to answer that based on the provided documents.'\n\n"
        )
        if context:
            prompt += "Context:\n" + "\n---\n".join(context)
        else:
            prompt += "Context:\nNo documents have been uploaded yet."
        return prompt


def get_llm(provider: str, api_key: str) -> LLMProvider:
    """
    Factory function to get the appropriate LLM provider.
    Falls back to environment variables if no API key is set by user, useful for a demo mode.
    """
    if not api_key:
        api_key = os.environ.get(f"{provider.upper()}_API_KEY", "")
        
    if provider.lower() == "openai":
        return OpenAILLM(api_key)
    elif provider.lower() == "groq":
        return GroqLLM(api_key)
    else:
        raise ValueError("Unsupported provider. Choose 'openai' or 'groq'.")
