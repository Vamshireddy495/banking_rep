from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    account_type:str
    initial_balance: Optional[float] = 0.0

class AccountResponse(BaseModel):
    id: int
    balance: float
    account_type: str
    
model_config = {
    "from_attributes": True
}