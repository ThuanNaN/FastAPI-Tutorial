"""Logic nghiệp vụ — topic 12: service pattern."""
from sqlalchemy.orm import Session

from app.models import Book
from app.exceptions import InsufficientStockError, BookNotFoundError


def get_book(db: Session, book_id: int) -> Book:
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundError(book_id)
    return book


def buy_book(db: Session, book_id: int) -> Book:
    book = get_book(db, book_id)
    if not book.in_stock:
        raise InsufficientStockError(book.title)
    return book