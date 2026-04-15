from typing import List
from sentence_transformers import SentenceTransformer

_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

def chunk_text(text: str, chunk_words: int = 400, overlap: int = 50) -> List[str]:
    """
    Chunks text into roughly word-based segments. 
    400 words is a safe proxy for ~500 tokens.
    """
    words = text.split()
    chunks = []
    i = 0
    if not words:
        return chunks
        
    while i < len(words):
        chunk = words[i : i + chunk_words]
        chunks.append(" ".join(chunk))
        i += chunk_words - overlap
        # Prevent infinite loop if chunk_words <= overlap
        if chunk_words <= overlap:
            break
            
    return chunks

def generate_embeddings(chunks: List[str]):
    """
    Generates vector embeddings for a list of text chunks.
    Returns a numpy array.
    """
    if not chunks:
        import numpy as np
        return np.array([])
    embeddings = get_embedder().encode(chunks, convert_to_numpy=True)
    return embeddings

def embed_query(query: str):
    """
    Generate embedding for a single query.
    """
    return get_embedder().encode([query], convert_to_numpy=True)[0]
