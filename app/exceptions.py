"""Error handling — topic 9: exception nghiệp vụ + handler riêng."""
from fastapi import Request, status
from fastapi.responses import JSONResponse


class BookNotFoundError(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id
        super().__init__(f"Sách {book_id} không tồn tại")


async def book_not_found_handler(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "BOOK_NOT_FOUND", "book_id": exc.book_id},
    )


class InsufficientStockError(Exception):
    def __init__(self, title: str):
        self.title = title
        super().__init__(f"Sách '{title}' đã hết hàng")


async def insufficient_stock_handler(request: Request, exc: InsufficientStockError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "INSUFFICIENT_STOCK", "title": exc.title},
    )