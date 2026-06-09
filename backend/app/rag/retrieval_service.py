import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Tuple
from ..models import DocumentChunk, VectorEmbedding
from .embedding_service import get_embedding_service
from ..config import get_settings

settings = get_settings()


class RetrievalService:
    @staticmethod
    async def retrieve_chunks(
        db: AsyncSession,
        query: str,
        document_ids: List[str],
        top_k: int = 10,
        similarity_threshold: float = 0.6
    ) -> List[Tuple]:
        embedding_service = get_embedding_service()
        query_embedding = embedding_service.embed_text(query)

        stmt = select(DocumentChunk).where(DocumentChunk.document_id.in_(document_ids))
        result = await db.execute(stmt)
        chunks = result.scalars().all()

        chunk_scores = []
        for chunk in chunks:
            if chunk.embeddings:
                embedding_bytes = chunk.embeddings[0].embedding
                chunk_embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
                similarity = embedding_service.similarity(query_embedding, chunk_embedding)

                if similarity >= similarity_threshold:
                    chunk_scores.append((chunk, similarity))

        chunk_scores.sort(key=lambda x: x[1], reverse=True)

        return chunk_scores[:top_k]

    @staticmethod
    async def store_embedding(
        db: AsyncSession,
        chunk_id: str,
        embedding: np.ndarray
    ) -> None:
        embedding_bytes = embedding.astype(np.float32).tobytes()

        vector_embedding = VectorEmbedding(
            chunk_id=chunk_id,
            embedding=embedding_bytes,
            embedding_model="sentence-transformers/all-minilm-l6-v2"
        )

        db.add(vector_embedding)
        await db.commit()

    @staticmethod
    async def get_embeddings_for_document(
        db: AsyncSession,
        document_id: str
    ) -> None:
        embedding_service = get_embedding_service()

        stmt = select(DocumentChunk).where(DocumentChunk.document_id == document_id)
        result = await db.execute(stmt)
        chunks = result.scalars().all()

        for chunk in chunks:
            embedding = await embedding_service.embed_text(chunk.text_content)
            await RetrievalService.store_embedding(db, str(chunk.id), embedding)
