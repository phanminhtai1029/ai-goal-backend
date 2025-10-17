from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import users, goals

# Dòng này sẽ tạo các bảng trong database nếu chúng chưa tồn tại
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
    # Chúng ta sẽ không dùng danh sách tĩnh nữa, mà dùng regex ở dưới
]

# Biểu thức chính quy (regex) để khớp với TẤT CẢ các URL của Vercel
# Bao gồm cả URL preview và URL production
# Nó sẽ khớp với https://ai-goal-frontend.vercel.app VÀ https://ai-goal-frontend-....vercel.app
vercel_regex = r"https?://ai-goal-frontend.*\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=vercel_regex, # Thêm regex vào đây để cho phép tất cả các URL của Vercel
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Gắn các router vào ứng dụng chính
app.include_router(users.router, prefix="/auth", tags=["Authentication"])
app.include_router(goals.router, prefix="/goals", tags=["Goals"])


@app.get("/")
def read_root():
    return {"message": "Welcome to AI Goal Assistant API - v2!"}

