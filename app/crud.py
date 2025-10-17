from sqlalchemy.orm import Session
from . import models, schemas, auth
from datetime import datetime

# --- User CRUD ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Goal CRUD ---

def get_goals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Goal).filter(models.Goal.owner_id == user_id).offset(skip).limit(limit).all()

def create_user_goal(db: Session, goal: schemas.GoalCreate, user_id: int):
    # SỬA LỖI DỨT ĐIỂM Ở ĐÂY:
    # Thay vì dựa vào giá trị mặc định, chúng ta sẽ gán một cách tường minh
    # đối tượng ENUM 'GoalStatus.pending' khi tạo mục tiêu mới.
    # Điều này đảm bảo SQLAlchemy gửi đúng kiểu dữ liệu cho database.
    db_goal = models.Goal(
        content=goal.content,
        due_date=goal.due_date,
        owner_id=user_id,
        status=models.GoalStatus.pending # Gán tường minh
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal_status(db: Session, goal_id: int, user_id: int, status: models.GoalStatus):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.owner_id == user_id).first()
    if db_goal:
        db_goal.status = status
        if status == models.GoalStatus.completed:
            db_goal.completed_at = datetime.utcnow()
        else:
            db_goal.completed_at = None
        db.commit()
        db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int, user_id: int):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id, models.Goal.owner_id == user_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
    return db_goal
