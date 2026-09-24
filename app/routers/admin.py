"""Admin router — topic 13: require_roles, role-based access."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_admin
from app.models import User
from app.schemas import UserOut

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
async def list_users(db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    """Topic 13 — require admin. Trả danh sách user."""
    return db.query(User).all()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db), _admin: User = Depends(get_current_admin)):
    """Topic 13 — admin xóa user."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không tồn tại")
    db.delete(user)
    db.commit()
    return None