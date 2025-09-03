#User-related routes
from fastapi import HTTPException, APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.dependencies import get_current_active_user, get_db

router = APIRouter()

#Get user 
@router.get("/me",response_model=UserResponse)
def read_user_info(current_user:User = Depends(get_current_active_user),
                   db:Session = Depends(get_db)):
    return current_user

#Update user
@router.put("/me",response_model=UserResponse)
def update_user(user_update:UserUpdate,
                db:Session = Depends(get_db),
                current_user:User = Depends(get_current_active_user)):
    
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.email:
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    return current_user