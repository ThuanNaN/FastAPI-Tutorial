"""Custom middleware — topic 10: log + đo thời gian xử lý."""
import time


async def add_process_time_header_middleware(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.4f} sec"
    print(f"→ {request.method} {request.url.path} ({process_time:.4f}s)")
    return response