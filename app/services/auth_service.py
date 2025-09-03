#Business Logic
#create user User(), hashpassword security/create_hash_pasword()
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core import security
from app.schemas.user import UserCreate, UserResponse

def create_user(user_data: UserCreate, db: Session) -> User:
    
    # existing_user = Session.query(User).filter(User.email == user_data.email).first()
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail = "Email registered")
    #Hash-user_input password 
    hashed_password = security.get_password_hash(user_data.password)

    user = User(email = user_data.email,   # new_object (User:instance)
                hashed_password = hashed_password,
                full_name = user_data.full_name
                ) 
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#Authenticate user
def authenticate_user(username:str,password:str, db:Session) -> User:

    user = db.query(User).filter(User.email == username).first() # Creates new_instance for USER 

    if not user:
        return None
        
    if not security.verify_password(password, user.hashed_password):
        return None
    
    return user



