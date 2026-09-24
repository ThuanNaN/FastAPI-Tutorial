"""Kết nối CSDL với SQLAlchemy 2.0 — topic 14.

- engine: quản lý kết nối.
- SessionLocal: nhà máy tạo session (mỗi request 1 session qua get_db).
- Base: lớp cơ sở cho các model.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    """Tạo bảng nếu chưa có (demo nhanh — production dùng Alembic, topic 14/19)."""
    import app.models  # noqa: F401  # đăng ký model trước khi create_all

    Base.metadata.create_all(bind=engine)