from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    session_id: Optional[UUID] = None
    query: str
    document_ids: List[UUID]
    stream: bool = False


class SourceDocument(BaseModel):
    document_id: UUID
    chunk_id: UUID
    similarity_score: float
    text_snippet: str


class ChatResponse(BaseModel):
    message_id: UUID
    response: str
    sources: List[SourceDocument]
    tokens_used: int
    response_time_ms: int


class ChatMessageResponse(BaseModel):
    id: UUID
    user_query: str
    assistant_response: Optional[str]
    source_documents: List[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: UUID
    title: Optional[str]
    document_ids: List[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatSessionCreateRequest(BaseModel):
    title: Optional[str] = None
    document_ids: List[UUID]


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]
    total: int
