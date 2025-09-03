from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core import security
from app.services import auth_service
from app.schemas.user import UserCreate, UserResponse
from app.core.database import SessionLocal
from app.models.user import User
from app.dependencies import get_current_active_user, get_db

router = APIRouter()

@router.post("/register",response_model=UserResponse)
def register_user(user:UserCreate, db:Session = Depends(get_db)):

    new_user = auth_service.create_user(user,db)
    return new_user


@router.post("/login")
def login_user(form_data:OAuth2PasswordRequestForm = Depends(), #Depends() is FastAPI’s way to declare a dependency. Hey, I need some data or logic before running this function. Please run that and give me the result.Please automatically create an instance of OAuth2PasswordRequestForm from the incoming request.
               db: Session = Depends(get_db)
            ):
    user = auth_service.authenticate_user(form_data.username, form_data.password, db)

    #check user credentials
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email_id or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    #create valid token
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data ={"sub":user.email},
                                                expires_delta = access_token_expires)
    
    return {"access_token":access_token, "token_type":"bearer"}




@router.get("/me")
def user_info(current_user:User = Depends(get_current_active_user)):
    
    return{"id":current_user.id,
           "email":current_user.email,
           "full_name":current_user.full_name
           }