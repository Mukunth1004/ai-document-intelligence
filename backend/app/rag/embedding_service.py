import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-minilm-l6-v2"):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def embed_text(self, text: str) -> np.ndarray:
        embeddings = self.model.encode([text], convert_to_numpy=True)
        return embeddings[0]

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)

    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


embedding_service = None


def get_embedding_service():
    global embedding_service
    if embedding_service is None:
        embedding_service = EmbeddingService()
    return embedding_service
