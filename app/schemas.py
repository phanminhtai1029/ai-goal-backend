from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime
from .models import GoalStatus # Quan trọng: Import Enum từ models

# --- Schemas cho Goal ---

class GoalBase(BaseModel):
    content: str
    due_date: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    owner_id: int
    status: GoalStatus # Sử dụng GoalStatus thay vì str
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# --- Schemas cho User ---

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    # Thêm validation cho password ở đây luôn cho nhất quán
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    is_active: bool
    pushover_user_key: Optional[str] = None
    goals: List[Goal] = []
    model_config = ConfigDict(from_attributes=True)

# --- Schemas cho Authentication (Phần bị thiếu) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

