import httpx
import numpy as np
import asyncio
from typing import List
from ..config import get_settings

settings = get_settings()


class EmbeddingService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction"
        self.model = "sentence-transformers/all-minilm-l6-v2"

    async def embed_text(self, text: str) -> np.ndarray:
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/{self.model}",
                    headers=headers,
                    json={"inputs": text},
                    timeout=30.0
                )
                embeddings = response.json()
                if isinstance(embeddings, list):
                    return np.array(embeddings[0])
                return np.array(embeddings)
        except Exception as e:
            print(f"Embedding error: {e}")
            raise

    async def embed_texts(self, texts: List[str]) -> np.ndarray:
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/{self.model}",
                    headers=headers,
                    json={"inputs": texts},
                    timeout=30.0
                )
                embeddings = response.json()
                return np.array(embeddings)
        except Exception as e:
            print(f"Embedding error: {e}")
            raise

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        try:
            a = np.array(a).flatten()
            b = np.array(b).flatten()
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))
        except Exception as e:
            print(f"Similarity error: {e}")
            return 0.0

    @staticmethod
    def similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        return EmbeddingService.cosine_similarity(embedding1, embedding2)


embedding_service = None


def get_embedding_service():
    global embedding_service
    if embedding_service is None:
        if not settings.huggingface_api_key:
            raise ValueError("HUGGINGFACE_API_KEY environment variable not set")
        embedding_service = EmbeddingService(settings.huggingface_api_key)
    return embedding_service
