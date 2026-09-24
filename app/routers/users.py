"""Users router — topic 4 & 5: path/query params, request body, response model.

Demo extra: endpoint /users/by-name/{username} phải khai báo TRƯỚC /users/{user_id}
(quy tắc route tĩnh trước route động — topic 3).
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import User
from app.schemas import UserCreate, UserOut
from app.security import hash_password

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/by-name/{username}", response_model=UserOut)
async def get_user_by_name(username: str, db: Session = Depends(get_db)):
    """Route TĨNH — đặt trước route động /users/{user_id}."""
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không tồn tại")
    return user


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter((User.username == data.username) | (User.email == data.email)).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username hoặc email đã tồn tại")
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    verbose: bool = Query(default=False, description="Chỉ để demo query param"),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không tồn tại")
    return user