from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import users, goals

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trợ lý Mục tiêu AI API",
    description="API cho ứng dụng quản lý mục tiêu học tập và công việc.",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(goals.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to AI Goal Assistant API"}

