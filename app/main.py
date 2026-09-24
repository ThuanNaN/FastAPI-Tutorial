"""App factory — topic 12 & 10: tạo app, middleware, CORS, include router."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import init_db
from app.exceptions import (
    BookNotFoundError,
    InsufficientStockError,
    book_not_found_handler,
    insufficient_stock_handler,
)
from app.middleware import add_process_time_header_middleware
from app.routers import admin, auth, books, streaming, uploads, users

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # tạo bảng khi startup (demo; production dùng Alembic)
    yield


app = FastAPI(
    title=settings.app_name,
    description="Project tổng hợp FastAPI — áp dụng topic 1-17.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Middleware (topic 10) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*.example.com"])
app.middleware("http")(add_process_time_header_middleware)

# --- Exception handlers (topic 9) ---
app.add_exception_handler(BookNotFoundError, book_not_found_handler)
app.add_exception_handler(InsufficientStockError, insufficient_stock_handler)

# --- Static files (topic 8) ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Routers (topic 12) ---
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(uploads.router)
app.include_router(streaming.router)
app.include_router(admin.router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Chào mừng đến với FastAPI Bookstore!", "docs": "/docs"}