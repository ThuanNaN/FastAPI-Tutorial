"""Streaming & WebSocket & BackgroundTasks router — topic 15."""
import asyncio
import os

from fastapi import APIRouter, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.deps import get_db

router = APIRouter(prefix="/api/stream", tags=["streaming"])


class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """Topic 15 — WebSocket hai chiều + broadcast."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"→ {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def _iter_book_notes():
    """Generator cho streaming demo."""
    for i in range(1, 6):
        yield f"dòng {i}\n"
        asyncio.sleep(0.2)


@router.get("/notes")
async def stream_notes():
    """Topic 15 — StreamingResponse."""
    return StreamingResponse(_iter_book_notes(), media_type="text/plain")


@router.get("/download/{filename}")
async def download_file(filename: str):
    """Topic 15 — FileResponse."""
    path = os.path.join("uploads", filename)
    if not os.path.exists(path):
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File không tồn tại")
    return FileResponse(path, filename=filename)


def _send_email_task(email: str, msg: str):
    """Background task mẫu."""
    with open("uploads/email_log.txt", "a") as f:
        f.write(f"{email}: {msg}\n")


@router.post("/notify")
async def notify(email: str, background_tasks: BackgroundTasks):
    """Topic 15 — BackgroundTasks chạy sau khi trả response."""
    background_tasks.add_task(_send_email_task, email, "Thông báo từ Bookstore")
    return {"message": "Đã nhận, sẽ xử lý sau"}