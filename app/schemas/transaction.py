from pydantic import BaseModel
from typing import Optional
from datetime import datetime

def TransactionCreate(BaseModel):
    
    from_account_id: int
    to_account_id: int
    amount: float
    type: str

def TransactionOut(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    timestamp: datetime
    type: str
    received_amount: float

    class Config:
        orm_mode = True
