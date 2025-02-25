import os
import json
import numpy as np
import logging
from typing import List, Tuple
from src.api import embed_texts
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger('search')

class SearchEngine:
    def __init__(self, embeddings_file: str):
        self.embeddings_file = embeddings_file
        self.embeddings = self.load_embeddings()

    def load_embeddings(self):
        if not os.path.exists(self.embeddings_file):
            logger.error("Embeddings file not found!")
            return {}

        with open(self.embeddings_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_query_embedding(self, query: str) -> List[float]:
        response = embed_texts([query], 'query')
        if "embeddings" in response and isinstance(response["embeddings"], list) and response["embeddings"]:
            return response["embeddings"][0]
        else:
            logger.error("Failed to generate embedding for query")
            return []

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        query_embedding = self.get_query_embedding(query)
        if not query_embedding:
            return []

        query_vector = np.array(query_embedding).reshape(1, -1)
        results = []

        for doc_name, doc_embedding in self.embeddings.items():
            doc_vector = np.array(doc_embedding).reshape(1, -1)
            similarity = cosine_similarity(query_vector, doc_vector)[0][0]
            results.append((doc_name, similarity))

        results.sort(key=lambda x: x[1], reverse=True)  # Sort by highest similarity
        return results[:top_k]

