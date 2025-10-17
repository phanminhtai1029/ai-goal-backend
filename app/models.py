import enum
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Boolean,
                          Enum as SQLEnum)
from sqlalchemy.orm import relationship
from .database import Base

# Định nghĩa Python Enum như cũ
class GoalStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    pushover_user_key = Column(String, nullable=True)
    goals = relationship("Goal", back_populates="owner")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    content = Column(String, index=True)
    due_date = Column(DateTime, nullable=True)
    
    # GIẢI PHÁP DỨT ĐIỂM LÀ ĐÂY: native_enum=False
    # Dòng này chỉ thị cho SQLAlchemy không tạo kiểu ENUM đặc biệt của PostgreSQL.
    # Thay vào đó, nó sẽ tạo một cột VARCHAR với một quy tắc CHECK,
    # cách làm này đáng tin cậy và tương thích hơn rất nhiều.
    status = Column(SQLEnum(GoalStatus, native_enum=False), default=GoalStatus.pending, nullable=False)
    
    completed_at = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="goals")

