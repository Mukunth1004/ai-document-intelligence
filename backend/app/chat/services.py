from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from ..models import ChatSession, ChatMessage
from ..rag.retrieval_service import RetrievalService
from ..rag.gemini_client import get_gemini_client
from ..config import get_settings

settings = get_settings()


class ChatService:
    @staticmethod
    async def create_session(
        db: AsyncSession,
        user_id: str,
        title: str = None,
        document_ids: List[UUID] = None
    ) -> ChatSession:
        session = ChatSession(
            user_id=user_id,
            title=title,
            document_ids=document_ids or []
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_session(
        db: AsyncSession,
        session_id: str,
        user_id: str
    ) -> ChatSession:
        stmt = select(ChatSession).where(
            (ChatSession.id == session_id) & (ChatSession.user_id == user_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_sessions(
        db: AsyncSession,
        user_id: str,
        limit: int = 50
    ):
        stmt = select(ChatSession).where(ChatSession.user_id == user_id).order_by(
            ChatSession.updated_at.desc()
        ).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def delete_session(
        db: AsyncSession,
        session_id: str,
        user_id: str
    ) -> bool:
        stmt = select(ChatSession).where(
            (ChatSession.id == session_id) & (ChatSession.user_id == user_id)
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            return False

        await db.delete(session)
        await db.commit()
        return True

    @staticmethod
    async def get_chat_history(
        db: AsyncSession,
        session_id: str,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ):
        session = await ChatService.get_session(db, session_id, user_id)
        if not session:
            return None, 0

        stmt = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(
            ChatMessage.created_at
        ).offset(offset).limit(limit)
        result = await db.execute(stmt)
        messages = result.scalars().all()

        stmt = select(ChatMessage).where(ChatMessage.session_id == session_id)
        result = await db.execute(stmt)
        total = len(result.scalars().all())

        return messages, total

    @staticmethod
    async def process_query(
        db: AsyncSession,
        session_id: str,
        user_id: str,
        query: str,
        document_ids: List[UUID]
    ):
        session = await ChatService.get_session(db, session_id, user_id)
        if not session:
            session = await ChatService.create_session(db, user_id, document_ids=document_ids)

        retrieved_chunks = await RetrievalService.retrieve_chunks(
            db=db,
            query=query,
            document_ids=[str(doc_id) for doc_id in document_ids],
            top_k=settings.top_k_chunks,
            similarity_threshold=settings.similarity_threshold
        )

        context = "\n\n".join([
            f"Document: {chunk.document.file_name}\nChunk {chunk.chunk_index}:\n{chunk.text_content}"
            for chunk, _ in retrieved_chunks
        ])

        gemini_client = get_gemini_client()
        response = await gemini_client.generate_response(
            query=query,
            context=context
        )

        source_ids = [str(chunk.document_id) for chunk, _ in retrieved_chunks]
        chat_message = ChatMessage(
            session_id=session.id,
            user_query=query,
            assistant_response=response,
            source_documents=source_ids
        )

        db.add(chat_message)
        await db.commit()
        await db.refresh(chat_message)

        return chat_message, [(chunk, score) for chunk, score in retrieved_chunks]
