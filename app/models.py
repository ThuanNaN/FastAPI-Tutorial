"""ORM models — SQLAlchemy 2.0 style (Mapped / mapped_column) — topic 14."""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user")  # admin | user
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    books: Mapped[list["Book"]] = relationship(back_populates="owner")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column()
    in_stock: Mapped[bool] = mapped_column(default=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped[User] = relationship(back_populates="books")