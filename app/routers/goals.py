from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List

from .. import schemas, crud, models, auth
from ..database import get_db

router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/", response_model=schemas.Goal)
def create_goal(
    goal: schemas.GoalCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_user_goal(db=db, goal=goal, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Goal])
def read_goals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    goals = crud.get_goals_for_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return goals

@router.put("/{goal_id}/complete", response_model=schemas.Goal)
def mark_goal_as_complete(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_goal = crud.update_goal_status(db=db, goal_id=goal_id, user_id=current_user.id)
    if not updated_goal:
        raise HTTPException(status_code=404, detail="Goal not found or you don't have permission")
    return updated_goal

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted_goal = crud.delete_goal(db=db, goal_id=goal_id, user_id=current_user.id)
    if not deleted_goal:
         raise HTTPException(status_code=404, detail="Goal not found or you don't have permission")
    return {"ok": True}

