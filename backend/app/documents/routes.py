from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import uuid
from ..database import get_db
from ..models import Document, DocumentChunk
from .schemas import DocumentResponse, DocumentListResponse, DocumentUploadResponse, DocumentDetailResponse
from .services import DocumentService
from ..middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "txt", "docx", "md"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    temp_dir = "/tmp/documents"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")

    try:
        contents = await file.read()
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        file_size = os.path.getsize(temp_file_path)

        document = await DocumentService.create_document(
            db=db,
            user_id=str(current_user.id),
            file_name=file.filename,
            file_path=temp_file_path,
            file_size=file_size,
            file_type=file_ext
        )

        return DocumentUploadResponse(
            document_id=document.id,
            status=document.processing_status,
            estimated_time=30
        )
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    documents, total = await DocumentService.list_documents(
        db=db,
        user_id=str(current_user.id),
        page=page,
        limit=limit
    )

    return DocumentListResponse(
        documents=[DocumentResponse.from_orm(doc) for doc in documents],
        total=total,
        page=page
    )


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    document = await DocumentService.get_document(
        db=db,
        document_id=document_id,
        user_id=str(current_user.id)
    )

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    stmt = select(DocumentChunk).where(DocumentChunk.document_id == document_id)
    result = await db.execute(stmt)
    chunks = result.scalars().all()

    return DocumentDetailResponse(
        id=document.id,
        file_name=document.file_name,
        file_size=document.file_size,
        file_type=document.file_type,
        char_count=document.char_count,
        page_count=document.page_count,
        processing_status=document.processing_status,
        embedding_count=document.embedding_count,
        created_at=document.created_at,
        is_public=document.is_public,
        text_content=document.text_content[:500] if document.text_content else None,
        chunks=[DocumentChunkResponse.from_orm(chunk) for chunk in chunks]
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = await DocumentService.delete_document(
        db=db,
        document_id=document_id,
        user_id=str(current_user.id)
    )

    if not success:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}


@router.get("/{document_id}/preview")
async def get_document_preview(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    document = await DocumentService.get_document(
        db=db,
        document_id=document_id,
        user_id=str(current_user.id)
    )

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    preview_text = document.text_content[:500] if document.text_content else ""
    return {
        "preview_text": preview_text,
        "total_chars": document.char_count,
        "file_name": document.file_name
    }


@router.get("/{document_id}/chunks")
async def get_document_chunks(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    document = await DocumentService.get_document(
        db=db,
        document_id=document_id,
        user_id=str(current_user.id)
    )

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    stmt = select(DocumentChunk).where(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index)
    result = await db.execute(stmt)
    chunks = result.scalars().all()

    return {
        "chunks": [
            {
                "id": chunk.id,
                "index": chunk.chunk_index,
                "text": chunk.text_content,
                "tokens": chunk.token_count
            }
            for chunk in chunks
        ],
        "total": len(chunks)
    }
