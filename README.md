# FastAPI-Tutorial

VLAI FastAPI Tutorial — khóa học FastAPI đầy đủ bằng tiếng Việt, kèm **project tổng hợp** để áp dụng toàn bộ kiến thức từ topic 1 đến topic 17, và deploy ở topic cuối cùng.

## Mô tả project

Đây là một **REST API quản lý sách (Bookstore API)** xây dựng từng bước xuyên suốt khóa học — mỗi topic thêm một tính năng mới vào project:

| Tính năng | Description |
|---|---|
| **Auth** | Đăng nhập JWT (HS256), phân quyền admin/user |
| **Books CRUD** | Tạo, đọc, cập nhật, xoá sách với validation & search/filter |
| **Upload** | Tải lên ảnh bìa sách, giới hạn dung lượng |
| **Streaming** | WebSocket chat, StreamingResponse, BackgroundTasks |
| **DB** | SQLAlchemy 2.0 + SQLite (dev) / PostgreSQL (production) |
| **Tests** | pytest với TestClient, DB test tách biệt |
| **Docker** | Docker + docker-compose deploy production với nginx |

Code trong repo là project bạn xây từng bước qua mỗi topic — không phải project rỗng rồi fill vào sau, mà là code chạy được ngay từ đầu mỗi topic.

## Cấu trúc khóa học

Khóa học gồm **19 phần** theo 6 chặng. Mỗi phần có file code chạy được nằm trong repo này (thư mục `app/`), giải thích vì sao — đó chính là project "Bookstore API" bạn sẽ xây từng bước:

| Giai đoạn | Parts | Project: phần code tương ứng |
|---|---|---|
| **Nền tảng** | 1–3 | `pyproject.toml`, `app/main.py` — routing cơ bản |
| **Xử lý dữ liệu** | 4–7 | `app/schemas.py` — params, body, response model, validation |
| **Ứng dụng thực tế** | 8–10 | `app/routers/uploads.py`, `app/exceptions.py` — file upload, lỗi, middleware/CORS |
| **Kiến trúc** | 11–14 | `app/deps.py`, `app/database.py`, `app/models.py`, `app/routers/` — DI, router, auth, DB |
| **Nâng cao** | 15–17 | `app/routers/streaming.py`, `tests/` — WebSocket/streaming, testing, async |
| **Dự án tổng hợp** | 18 | Toàn bộ `app/` — lắp ghép mọi thứ thành một app hoàn chỉnh |
| **Kết thúc** | 19 | `Dockerfile`, `docker-compose.yml`, `nginx.conf` — deploy production |

> Project này chính là thứ bạn deploy ở phần cuối — không có project thì không có gì để deploy.

## Quick Start

```bash
# 1. Môi trường ảo
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# 2. Cài đặt dependencies
pip install -e ".[dev]"

# 3. Cấu hình
cp .env.example .env

# 4. Khởi tạo database + chạy
python -m app.scripts.init_db    # tạo bảng + seed dữ liệu demo
uvicorn app.main:app --reload
```

Mở trình duyệt:
- API: http://127.0.0.1:8000
- Docs tương tác (Swagger): http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Tài khoản demo

| Role | Username | Password |
|---|---|---|
| admin | `admin` | `admin123` |
| user | `user` | `user123` |

Lấy JWT: `POST /api/auth/login` (form `username` + `password`) → dùng nút **Authorize** trong Swagger.

## Chạy test

```bash
pytest -v
```

## Deploy (topic 19)

```bash
# Docker
docker build -t fastapi-bookstore .
docker compose up -d
```

Xem [README deploy](README-deploy.md) hoặc topic 19 để biết gunicorn/nginx chi tiết.

## Cấu trúc dự án

```
FastAPI-Tutorial/
├── app/
│   ├── __init__.py
│   ├── main.py            # app factory, middleware, CORS, include router
│   ├── config.py          # pydantic-settings (12-factor)
│   ├── database.py        # SQLAlchemy engine/session, Base
│   ├── models.py          # ORM models (User, Book)
│   ├── schemas.py         # Pydantic schemas (in/out)
│   ├── deps.py            # Dependency Injection (get_db, auth, role check)
│   ├── security.py        # hash mật khẩu + JWT
│   ├── exceptions.py      # custom exception handlers
│   ├── middleware.py      # custom middleware (process time header)
│   ├── routers/           # APIRouter theo nghiệp vụ
│   │   ├── __init__.py
│   │   ├── auth.py        # JWT login, /me
│   │   ├── users.py       # user management
│   │   ├── books.py       # CRUD books với validation & query params
│   │   ├── uploads.py     # UploadFile, size limit
│   │   ├── streaming.py   # WebSocket, StreamingResponse, BackgroundTasks
│   │   └── admin.py       # admin-only routes
│   ├── services/          # business logic layer
│   │   └── book_service.py
│   └── scripts/
│       └── init_db.py     # seed database demo (users + books)
├── tests/                 # pytest (topic 16)
│   ├── conftest.py        # TestClient setup, fixtures, test DB
│   ├── test_auth.py
│   ├── test_books.py
│   └── test_upload.py
├── uploads/               # runtime — file uploads được lưu ở đây
├── requirements.txt       # pip dependencies (dùng cho Docker build)
├── Dockerfile             # deploy (topic 19) — Python 3.12-slim
├── docker-compose.yml
├── nginx.conf
├── pyproject.toml         # package config + dev dependencies
├── .env.example
└── README-deploy.md
```

## Tech stack

| Layer | Technology |
|---|---|
| Framework | **FastAPI** 0.115+ |
| ORM | **SQLAlchemy** 2.0 |
| Validation | **Pydantic** v2 |
| Config | **pydantic-settings** (12-factor) |
| Auth | **JWT** (HS256) + **bcrypt** password hashing |
| Database | **SQLite** (dev) / **PostgreSQL** (production) |
| Async | `asyncio`, `aiofiles` |
| Testing | **pytest** + **httpx** TestClient |
| Container | **Docker** + **docker-compose** |
| Static files | FastAPI `StaticFiles` + `UploadFile` |

## Cấu hình (`.env`)

```env
DATABASE_URL=sqlite:///./bookstore.db
SECRET_KEY=change-me-to-a-long-random-string
DEBUG=false
```

Các trường cấu hình trong `app/config.py`:

| Biến | Mặc định | Mô tả |
|---|---|---|
| `app_name` | `"FastAPI Bookstore"` | Tên ứng dụng |
| `debug` | `False` | Chế độ debug |
| `database_url` | `sqlite:///./bookstore.db` | Connection string CSDL |
| `secret_key` | `CHANGE-ME-KEY-EXTERNAL` | Khóa ký JWT (≥ 32 ký tự) |
| `algorithm` | `HS256` | Thuật toán JWT |
| `access_token_expire_minutes` | `60` | Thời hạn access token |
| `max_upload_size_mb` | `10` | Dung lượng file upload tối đa |

## Phát triển & đóng gói

- **Dev**: `pip install -e ".[dev]"` dùng `pyproject.toml`
- **Docker**: `requirements.txt` được copy vào image (nhẹ hơn cho build)
- **Dockerfile** dùng `python:3.12-slim`
- **docker-compose.yml** có cả service app + PostgreSQL để test production-like

## Chạy test

Tests dùng `TestClient` với database in-memory SQLite tạm thời (không ảnh hưởng đến DB chính). `conftest.py` thiết lập test fixtures: `client`, `test_db`, `seeded_db`.

```bash
# Chạy tất cả tests
pytest -v

# Chạy test cụ thể
pytest tests/test_books.py -v
```
