from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime


class DocumentChunkResponse(BaseModel):
    id: UUID
    chunk_index: int
    text_content: str
    char_start: int
    char_end: int
    token_count: int

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: UUID
    file_name: str
    file_size: int
    file_type: str
    char_count: int
    page_count: Optional[int]
    processing_status: str
    embedding_count: int
    created_at: datetime
    is_public: bool

    class Config:
        from_attributes = True


class DocumentDetailResponse(DocumentResponse):
    text_content: Optional[str]
    chunks: List[DocumentChunkResponse] = []


class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int
    page: int


class DocumentUploadResponse(BaseModel):
    document_id: UUID
    status: str
    estimated_time: int
