import faiss
import numpy as np
import os
import json
from typing import List

INDEX_FILE = "index.faiss"
METADATA_FILE = "metadata.json"

class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = None
        self.metadata: List[str] = [] 

    def _initialize(self):
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.load()

    def add_texts(self, chunks: List[str], embeddings: np.ndarray):
        if len(chunks) == 0:
            return
        
        self._initialize()
        # Add to FAISS index
        self.index.add(embeddings)
        # Update metadata
        self.metadata.extend(chunks)
        self.save()

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[str]:
        self._initialize()
        if self.index.ntotal == 0:
            return []
        
        # Ensure query is 2D numpy array
        query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        # Adjust top_k if we have fewer elements
        k = min(top_k, self.index.ntotal)
        if k == 0:
            return []

        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

    def save(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False)

    def load(self):
        if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
            try:
                self.index = faiss.read_index(INDEX_FILE)
                with open(METADATA_FILE, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
            except Exception as e:
                print(f"Failed to load vector store: {e}")

# Global instance
vector_store = VectorStore(dimension=384)
