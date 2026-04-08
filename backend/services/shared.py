from backend.services.vector_store import VectorStore
from backend.services.llm import LLMService

# Singletons to be used across the application to ensure data consistency
vector_store = VectorStore()
llm_service = LLMService()
