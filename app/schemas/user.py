from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email:EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

model_config = {
    "from_attributes": True
}