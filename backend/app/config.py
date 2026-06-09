import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "AI Document Intelligence"
    app_version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost:5432/ai_doc_intelligence"
    )

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    refresh_token_expiration_days: int = 7

    # Google Gemini API
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = "gemini-pro"

    # Embeddings
    embedding_model: str = "sentence-transformers/all-minilm-l6-v2"
    embedding_dimension: int = 384

    # RAG
    chunk_size: int = 1024
    chunk_overlap: int = 204  # 20% of chunk_size
    similarity_threshold: float = 0.6
    top_k_chunks: int = 10
    max_context_tokens: int = 8000

    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds

    # File processing
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_file_types: list = ["pdf", "txt", "docx", "md"]

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
