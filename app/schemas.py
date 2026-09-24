"""Pydantic schemas — request body & response model — topic 5, 6, 7.

Quy tắc: tách schema đầu vào (Create) và đầu ra (Out) — không lộ password.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Users ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
    role: str = Field(default="user", pattern=r"^(admin|user)$")


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime


# ---------- Books ----------
class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: float = Field(gt=0, description="Giá phải lớn hơn 0")
    in_stock: bool = True


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: float | None = Field(default=None, gt=0)
    in_stock: bool | None = None


class BookOut(BaseModel):
    """Response model — không lộ owner_id? Ta giữ để minh họa; ở project thật
    có thể tách BookOut riêng cho client public."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    description: str | None
    price: float
    in_stock: bool
    owner_id: int


# ---------- Upload ----------
class UploadOut(BaseModel):
    filename: str
    content_type: str | None
    size: int