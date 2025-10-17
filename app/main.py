from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, goals
from fastapi.middleware.cors import CORSMiddleware

# Dòng này sẽ tự động tạo các bảng trong database nếu chúng chưa tồn tại
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trợ lý Mục tiêu AI API",
    description="API cho ứng dụng quản lý mục tiêu học tập và công việc.",
    version="1.0.0"
)

# --- CẤU HÌNH CORS ---
# THAY ĐỔI QUAN TRỌNG LÀ Ở ĐÂY
origins = [
    "http://localhost:5173",  # Cho phép local frontend
    "https://ai-goal-frontend-9ksykhrum-kources-projects.vercel.app", # THÊM DÒNG NÀY VÀO
    # Hãy thay thế bằng URL Vercel thực tế của bạn
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Chào mừng đến với API Trợ lý Mục tiêu AI!"}

# Gắn các router vào ứng dụng chính
app.include_router(users.router, prefix="/auth", tags=["Authentication"])
app.include_router(goals.router, prefix="/goals", tags=["Goals"])
