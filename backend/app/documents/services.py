import os
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import Document, DocumentChunk, User
from ..config import get_settings
from .file_processors import FileProcessor
from .chunking_service import ChunkingService

settings = get_settings()


class DocumentService:
    @staticmethod
    async def create_document(
        db: AsyncSession,
        user_id: str,
        file_name: str,
        file_path: str,
        file_size: int,
        file_type: str
    ) -> Document:
        text_content = FileProcessor.extract_text(file_path, file_type)
        char_count = len(text_content)

        document = Document(
            user_id=user_id,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            text_content=text_content,
            char_count=char_count,
            processing_status="processing"
        )

        db.add(document)
        await db.commit()
        await db.refresh(document)

        await DocumentService.process_document(db, document.id)

        return document

    @staticmethod
    async def process_document(db: AsyncSession, document_id: str) -> None:
        stmt = select(Document).where(Document.id == document_id)
        result = await db.execute(stmt)
        document = result.scalar_one_or_none()

        if not document:
            return

        try:
            chunks = ChunkingService.chunk_text(
                document.text_content,
                settings.chunk_size,
                settings.chunk_overlap
            )

            for idx, chunk in enumerate(chunks):
                doc_chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=idx,
                    text_content=chunk["text"],
                    char_start=chunk["char_start"],
                    char_end=chunk["char_end"],
                    token_count=chunk["token_count"]
                )
                db.add(doc_chunk)

            document.processing_status = "completed"
            document.embedding_count = len(chunks)
            await db.commit()
        except Exception as e:
            document.processing_status = "failed"
            await db.commit()
            print(f"Error processing document: {e}")

    @staticmethod
    async def get_document(db: AsyncSession, document_id: str, user_id: str) -> Document:
        stmt = select(Document).where(
            (Document.id == document_id) & (Document.user_id == user_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_documents(
        db: AsyncSession,
        user_id: str,
        page: int = 1,
        limit: int = 20
    ):
        stmt = select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
        result = await db.execute(stmt)
        total = len(result.scalars().all())

        offset = (page - 1) * limit
        stmt = select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(stmt)
        documents = result.scalars().all()

        return documents, total

    @staticmethod
    async def delete_document(db: AsyncSession, document_id: str, user_id: str) -> bool:
        stmt = select(Document).where(
            (Document.id == document_id) & (Document.user_id == user_id)
        )
        result = await db.execute(stmt)
        document = result.scalar_one_or_none()

        if not document:
            return False

        await db.delete(document)
        await db.commit()
        return True
