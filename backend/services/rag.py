from backend.schemas import ChatRequest
from backend.services.embeddings import embed_query
from backend.services.vector_store import vector_store
from backend.services.llm import get_llm

def run_rag_pipeline(request: ChatRequest) -> str:
    """
    Core RAG orchestrator:
    1. Embed query
    2. Search Top-K similarities in FAISS
    3. Construct LLM chain with context and handle the answer
    """
    # 1. Embed query sequence
    try:
        query_vector = embed_query(request.query)
    except Exception as e:
        return f"Error embedding query: {str(e)}"
    
    # 2. Retrieve top-3 contexts
    try:
        context_chunks = vector_store.search(query_vector, top_k=3)
    except Exception as e:
        return f"Error retrieving from vector store: {str(e)}"
    
    # 3. Retrieve LLM provider client
    try:
        llm = get_llm(request.provider, request.api_key)
    except Exception as e:
        return str(e)
        
    # 4. Generate intelligent response using the context
    answer = llm.generate_response(request.query, context_chunks, request.history)
    
    return answer
