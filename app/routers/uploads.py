"""Uploads router — topic 8: Form, UploadFile, static files."""
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.deps import get_db
from app.config import get_settings

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("", response_model=dict)
async def upload_book_cover(
    file: UploadFile = File(...),
    book_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """Topic 8 — UploadFile. Topic 4 — Book ID (path-like, ở đây là Form)."""
    settings = get_settings()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024

    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File quá lớn (tối đa {settings.max_upload_size_mb}MB)")

    # Lưu file an toàn — topic 8: chống path traversal
    import os, uuid
    safe_name = os.path.basename(file.filename or "unknown")
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", unique_name)
    async with open(file_path, "wb") as f:
        await f.write(content)

    return {"filename": file.filename, "content_type": file.content_type, "size": len(content), "saved_as": unique_name}