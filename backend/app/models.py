from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, UUID, ForeignKey, ARRAY, Float, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    api_key = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    quota_documents = Column(Integer, default=100)
    quota_queries = Column(Integer, default=10000)
    documents_used = Column(Integer, default=0)
    queries_used = Column(Integer, default=0)

    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    api_logs = relationship("APIUsageLog", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    s3_url = Column(String(512))
    text_content = Column(Text)
    char_count = Column(Integer)
    page_count = Column(Integer)
    processing_status = Column(String(50), default="pending")
    embedding_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_public = Column(Boolean, default=False)

    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer)
    text_content = Column(Text, nullable=False)
    char_start = Column(Integer)
    char_end = Column(Integer)
    token_count = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    document = relationship("Document", back_populates="chunks")
    embeddings = relationship("VectorEmbedding", back_populates="chunk", cascade="all, delete-orphan")


class VectorEmbedding(Base):
    __tablename__ = "vector_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False)
    embedding = Column(LargeBinary)
    embedding_model = Column(String(100), default="sentence-transformers/all-minilm-l6-v2")
    similarity_score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

    chunk = relationship("DocumentChunk", back_populates="embeddings")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255))
    document_ids = Column(ARRAY(UUID), default=[])
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_archived = Column(Boolean, default=False)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    user_query = Column(Text, nullable=False)
    assistant_response = Column(Text)
    source_documents = Column(ARRAY(UUID), default=[])
    response_tokens = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    session = relationship("ChatSession", back_populates="messages")


class APIUsageLog(Base):
    __tablename__ = "api_usage_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    endpoint = Column(String(255))
    method = Column(String(10))
    response_time_ms = Column(Integer)
    tokens_used = Column(Integer)
    status_code = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    user = relationship("User", back_populates="api_logs")
