import faiss
import numpy as np
import os
import pickle
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', index_name: str = 'faiss_index'):
        self.model = SentenceTransformer(model_name)
        # Use absolute path for reliability
        self.base_path = Path(__file__).parent.parent / "vector_store"
        self.index_path = self.base_path / f"{index_name}.index"
        self.pkl_path = self.base_path / f"{index_name}.pkl"
        
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = [] # Stores rows of text chunks
        
        # Ensure storage directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing index if it exists
        self.load()

    def add_documents(self, chunks: List[str]):
        if not chunks:
            logger.warning("No chunks provided to add_documents")
            return
            
        logger.info(f"Adding {len(chunks)} chunks to vector store")
        embeddings = self.model.encode(chunks)
        embeddings = np.array(embeddings).astype('float32')
        
        self.index.add(embeddings)
        self.metadata.extend(chunks)
        self.save()
        logger.info("Documents added and saved to disk")

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if self.index.ntotal == 0:
            logger.info("Search index is empty")
            return []
            
        logger.info(f"Searching for: '{query}'")
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        logger.info(f"Retrieved {len(results)} relevant chunks")
        return results

    def save(self):
        faiss.write_index(self.index, str(self.index_path))
        with open(self.pkl_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self):
        if self.index_path.exists() and self.pkl_path.exists():
            logger.info(f"Loading existing index from {self.index_path}")
            self.index = faiss.read_index(str(self.index_path))
            with open(self.pkl_path, 'rb') as f:
                self.metadata = pickle.load(f)
            logger.info(f"Index loaded with {len(self.metadata)} total chunks")
        else:
            logger.info("No existing index found, starting fresh")

    def reload(self):
        """Explicitly reloads the index from disk."""
        self.load()
