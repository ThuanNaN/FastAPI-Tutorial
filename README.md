# FastAPI-Tutorial

VLAI FastAPI Tutorial — khóa học FastAPI đầy đủ bằng tiếng Việt, kèm **project tổng hợp** để áp dụng toàn bộ kiến thức từ topic 1 đến topic 17, và deploy ở topic cuối cùng.

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
│   ├── database.py        # SQLAlchemy engine/session
│   ├── models.py          # ORM models
│   ├── schemas.py         # Pydantic schemas (in/out)
│   ├── deps.py            # Dependency Injection
│   ├── security.py        # hash mật khẩu + JWT
│   ├── exceptions.py      # custom exception handler
│   ├── middleware.py      # custom middleware
│   ├── routers/           # APIRouter theo nghiệp vụ
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── books.py
│   │   ├── uploads.py
│   │   ├── streaming.py
│   │   └── admin.py
│   └── services/          # logic nghiệp vụ
│       └── book_service.py
├── tests/                 # pytest (topic 16)
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_books.py
│   └── test_upload.py
├── static/                # static files (topic 8)
├── Dockerfile             # deploy (topic 19)
├── docker-compose.yml
├── nginx.conf
├── pyproject.toml
├── requirements.txt
├── .env.example
└── README-deploy.md
```