"""Books router — topic 4, 5, 6, 7: params, body, response model, validation."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_admin, get_current_user
from app.exceptions import BookNotFoundError, InsufficientStockError
from app.models import Book, User
from app.schemas import BookIn, BookOut, BookUpdate
from app.security import hash_password

router = APIRouter(prefix="/api/books", tags=["books"])


@router.get("", response_model=list[BookOut])
async def list_books(
    q: str | None = Query(default=None, description="Tìm kiếm theo tên"),
    min_price: float | None = Query(default=None, ge=0),
    in_stock: bool | None = None,
    db: Session = Depends(get_db),
):
    """Topic 4 — query params với Annotated + Query."""
    query = db.query(Book)
    if q:
        query = query.filter(Book.title.ilike(f"%{q}%"))
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if in_stock is not None:
        query = query.filter(Book.in_stock == in_stock)
    return query.all()


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(data: BookIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Topic 5 — Pydantic request body. Topic 7 — validation qua Field."""
    book = Book(**data.model_dump(), owner_id=current_user.id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Topic 6 — response_model."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundError(book_id)
    return book


@router.put("/{book_id}", response_model=BookOut)
async def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundError(book_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(book, key, val)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise BookNotFoundError(book_id)
    db.delete(book)
    db.commit()
    return None