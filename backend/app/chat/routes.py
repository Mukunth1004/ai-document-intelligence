from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..database import get_db
from ..middleware.auth import get_current_user
from .schemas import (
    ChatRequest, ChatResponse, ChatSessionCreateRequest,
    ChatSessionResponse, ChatHistoryResponse, SourceDocument
)
from .services import ChatService
from ..rag.gemini_client import get_gemini_client
import time
import json

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    start_time = time.time()

    session_id = chat_request.session_id or UUID(int=0)
    session = await ChatService.get_session(db, str(session_id), str(current_user.id))

    chat_message, retrieved_chunks = await ChatService.process_query(
        db=db,
        session_id=str(session_id) if session_id != UUID(int=0) else None,
        user_id=str(current_user.id),
        query=chat_request.query,
        document_ids=chat_request.document_ids
    )

    sources = [
        SourceDocument(
            document_id=chunk.document_id,
            chunk_id=chunk.id,
            similarity_score=score,
            text_snippet=chunk.text_content[:200]
        )
        for chunk, score in retrieved_chunks
    ]

    response_time_ms = int((time.time() - start_time) * 1000)

    return ChatResponse(
        message_id=chat_message.id,
        response=chat_message.assistant_response,
        sources=sources,
        tokens_used=0,
        response_time_ms=response_time_ms
    )


@router.post("/stream")
async def chat_stream(
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    async def generate():
        chat_message, retrieved_chunks = await ChatService.process_query(
            db=db,
            session_id=str(chat_request.session_id) if chat_request.session_id else None,
            user_id=str(current_user.id),
            query=chat_request.query,
            document_ids=chat_request.document_ids
        )

        gemini_client = get_gemini_client()

        async for chunk in gemini_client.stream_response(
            query=chat_request.query,
            context="\n\n".join([
                f"Document: {doc_chunk.document.file_name}\nChunk {doc_chunk.chunk_index}:\n{doc_chunk.text_content}"
                for doc_chunk, _ in retrieved_chunks
            ])
        ):
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        yield f"data: {json.dumps({'done': True, 'total_tokens': 0})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_history(
    session_id: str,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    messages, total = await ChatService.get_chat_history(
        db=db,
        session_id=session_id,
        user_id=str(current_user.id),
        limit=limit,
        offset=offset
    )

    if messages is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return ChatHistoryResponse(
        messages=[msg for msg in messages],
        total=total
    )


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    session_data: ChatSessionCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    session = await ChatService.create_session(
        db=db,
        user_id=str(current_user.id),
        title=session_data.title,
        document_ids=session_data.document_ids
    )

    return ChatSessionResponse(
        id=session.id,
        title=session.title,
        document_ids=session.document_ids,
        created_at=session.created_at,
        updated_at=session.updated_at
    )


@router.get("/sessions", response_model=list)
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    sessions = await ChatService.list_sessions(
        db=db,
        user_id=str(current_user.id)
    )

    return [
        ChatSessionResponse(
            id=session.id,
            title=session.title,
            document_ids=session.document_ids,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
        for session in sessions
    ]


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = await ChatService.delete_session(
        db=db,
        session_id=session_id,
        user_id=str(current_user.id)
    )

    if not success:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"message": "Session deleted successfully"}
