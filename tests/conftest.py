import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.deps import get_db

# ── Override database engine before importing app.main ──────────────────────────
# app.database creates engine/SessionLocal at import time from settings.database_url.
# We patch them so init_db() (called in app.main lifespan) creates tables on the
# test engine and all queries use the in-memory SQLite DB.
TEST_DB_URL = "sqlite:///./test_bookstore.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

import app.database

app.database.engine = test_engine
app.database.SessionLocal = TestingSessionLocal

from app.main import app


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def client():
    """FastAPI TestClient with the test database active."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_db():
    """Yield a fresh session bound to the test engine; drops tables after."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def seeded_db(test_db):
    """test_db with a demo user (username='user', password='user123') seeded."""
    from app.models import User
    from app.security import hash_password

    user = User(username="user", email="user@book.com", hashed_password=hash_password("user123"), role="user")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    yield test_db
