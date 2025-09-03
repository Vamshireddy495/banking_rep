from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):

    from_account_id: Optional[int]
    to_account_id: Optional[int]
    amount: Optional[float]
    #type: str

class TransactionOut(BaseModel):
    id: int
    
    from_account_id: int
    to_account_id: Optional[int]
    amount: Optional[float]

    timestamp: datetime
    type: str


class TransactionSummary(BaseModel):
    to_account_id: int
    amount: float

model_config = {
    "from_attributes": True
}