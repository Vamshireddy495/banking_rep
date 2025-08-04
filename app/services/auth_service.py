#Business Logic
#create user User(), hashpassword security/create_hash_pasword()
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core import security
from app.schemas.user import UserCreate, UserOut

def create_user(user_data: UserCreate, db: Session) -> User:
    
    # existing_user = Session.query(User).filter(User.email == user_data.email).first()
    if Session.query(User).filter(User.email == user_data.email):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail = "Email registered")
    
    hashed_password = security.get_password_hash(user_data.password)

    user = User(email = user_data.email,
                hashed_password = hashed_password,
                full_name = user_data.full_name
                ) 
    
    Session.add(user)
    Session.commit()
    Session.refresh(user)
    return user

#Authenticate user
def authenticate_user(email:str,password:str, db:Session) -> User:

    user = Session.query(User).filter(User.email == email).first()

    if not user:
        return None
        
    if not security.verify_password(password, user.hashed_password):
        return None
    
    return None



