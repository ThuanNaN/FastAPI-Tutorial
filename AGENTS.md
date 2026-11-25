# AGENTS.md

Bookstore REST API (FastAPI + SQLAlchemy 2.0 + Pydantic v2) — project đi kèm khóa FastAPI của VLAI
(https://vlai.aivietnam.edu.vn/tutorials/fastapi-tutorial). Đây là **phiên bản chạy được hoàn chỉnh** của project, dùng làm nguồn đối chiếu cho nội dung bài học.

## Chạy

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
python -m app.scripts.init_db     # tạo bảng + seed dữ liệu demo
uvicorn app.main:app --reload     # http://127.0.0.1:8000/docs
pytest -v                         # test dùng SQLite in-memory, không đụng DB chính
```

## Quy ước

- Cấu hình đọc từ `app/config.py` (pydantic-settings); không hard-code secret.
- Logic nghiệp vụ nằm trong `app/services/`, router chỉ nhận request và trả response.
- Mọi thay đổi hành vi (endpoint, status code, mặc định cấu hình) phải cập nhật README và chạy `pytest -v`.
- Bài học dùng lệnh, đầu ra và giá trị cấu hình từ repo này: đổi chúng thì bài học cần được sửa theo.
