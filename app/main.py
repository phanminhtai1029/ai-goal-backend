from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import users, goals

# Dòng này sẽ tạo các bảng trong database nếu chúng chưa tồn tại
# Sau khi dùng Alembic hoặc các công cụ migration khác thì có thể bỏ đi
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trợ lý Mục tiêu AI API",
    description="API cho ứng dụng quản lý mục tiêu học tập và công việc.",
    version="1.0.0"
)

# --- CẤU HÌNH CORS ---
# Danh sách các "địa chỉ" được phép gọi đến API
origins = [
    "http://localhost:5173",  # Địa chỉ của Frontend khi chạy local
    "https://ai-goal-frontend-9ksykhrum-kources-projects.vercel.app" # Quan trọng: Thay bằng URL Vercel của bạn
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Cho phép tất cả các phương thức (GET, POST, etc.)
    allow_headers=["*"], # Cho phép tất cả các header
)

# Gắn các router vào ứng dụng chính
app.include_router(users.router, prefix="/auth", tags=["Authentication"])
app.include_router(goals.router, prefix="/goals", tags=["Goals"])


@app.get("/")
def read_root():
    return {"message": "Chào mừng đến với Trợ lý Mục tiêu AI API!"}

