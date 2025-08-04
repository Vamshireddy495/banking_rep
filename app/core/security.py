# Hashing/JWT Creation/Validation
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY','Banking_security_key')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',30))

#Password Hashing 1)Verify 2)Generate
pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def get_password_hash(password:str) -> str:
    return CryptContext(schemes= ['bcrypt'],deprecated='auto').hash(password)

def verify_password(plain_password:str, hashed_password:str) -> str:
    return CryptContext(schems= ['bcrypt']).verify(plain_password,hashed_password)



#JSON Web Token 1)Creation 2)Validation

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp':expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encode_jwt


def validate_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        return payload
    except JWTError:
        raise Exception(f"Token validation failed: {str(JWTError)}")
    
    

