# Deploy FastAPI Bookstore

## Build
```bash
docker build -t fastapi-bookstore .
docker compose up -d
```

## Production
- Gunicorn + UvicornWorker: `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000`
- Nginx reverse proxy: copy `nginx.conf` to server block
- SSL: Certbot or CDN
- Env: copy `.env.example` → `.env`, set real `SECRET_KEY`, `DATABASE_URL` (PostgreSQL)
- Migrations: `alembic upgrade head`
- Health: `GET /` returns 200