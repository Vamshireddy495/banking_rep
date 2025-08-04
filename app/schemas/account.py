from pydantic import BaseModel
from typing import Optional

def AccountCreate(BaseModel):
    initial_balance: Optional[float] = 0.0
    type:str

def AccountOut(BaseModel):
    id: int
    balance: float
    account_type: str
    
    class Config:
        orm_mode = True