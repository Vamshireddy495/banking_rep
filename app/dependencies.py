from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core import security
from app.core.database import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)) -> User: #needs token, it then asks oauth2_scheme, it will tell fastapi you can find it "/auth/login"
                                                                                                #login() returns {"access_token":"<jwt-token","token_type":"bearer"}, now, get_current_user USES token to check if it is valid.
                                                                                                #payload = security.validate_access_token(token) now payload.         *JWT has 3 parts <Header>.<Payload>.<Signature>*                  #it will check email from payload.get("sub"), now, it extracts user from db.
                                                                                                                                                                #<Algorithm & Type Info>.<Claims like "sub","exp","role">.<Verifies token integrity>	
    credential_exception = HTTPException(
                                            status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail= "Invalid credentials",
                                            headers={"WWW-Authenticate":"Bearer"}
                                        )

    payload = security.validate_access_token(token)
    if payload is None:
        raise credential_exception
    
    email:str = payload.get("sub")
    if email is None:
        raise credential_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credential_exception

    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
