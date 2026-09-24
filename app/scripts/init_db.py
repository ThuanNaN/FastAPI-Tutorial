"""Seed database với users/books demo — topic 2 & 14.

Chạy: python -m app.scripts.init_db
"""
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import User
from app.schemas import BookIn
from app.security import hash_password


def seed():
    init_db()
    db: Session = SessionLocal()
    try:
        # Seed users
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(username="admin", email="admin@book.com", hashed_password=hash_password("admin123"), role="admin")
            db.add(admin)
        if not db.query(User).filter(User.username == "user").first():
            user = User(username="user", email="user@book.com", hashed_password=hash_password("user123"), role="user")
            db.add(user)

        # Seed books
        books_data = [
            BookIn(title="Nhập môn FastAPI", author="VLAI Lab", description="Cuốn sách nhập môn", price=0),
            BookIn(title="Deep Learning với PyTorch", author="VLAI Lab", description="Hướng dẫn DL", price=0),
        ]
        for book_data in books_data:
            if not db.query(Book).filter(Book.title == book_data.title).first():
                book = Book(**book_data.model_dump(), owner_id=1)
                db.add(book)
        db.commit()
        print("✅ Đã seed dữ liệu demo: admin/admin123, user/user123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()