#Deposit, Withdraw, Transfer
from fastapi import HTTPException,status, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionSummary
from app.models.user import User
from app.dependencies import get_db, get_current_active_user

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

#Depost API
@router.post("/deposit", response_model = TransactionSummary)
def deposit(transaction_amt:TransactionSummary,
            db:Session = Depends(get_db),
            current_user:User = Depends(get_current_active_user)):
    
    
    account = db.query(Account).filter(Account.user_id == current_user.id,
                                       Account.id == transaction_amt.to_account_id).first()
    
    if not account:
        raise HTTPException(status_code = 404, detail="Account not found")
    
    if transaction_amt.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = "Amount should be positive!")
    
    account.balance += transaction_amt.amount
    

    transaction = Transaction(to_account_id = account.id,
                              type= "deposit",
                              amount = transaction_amt.amount,
                              timestamp = datetime.utcnow())


    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

# Withdraw API
@router.post("/withdraw", response_model=TransactionOut)
def withdraw(transaction_amt:TransactionCreate,
             db:Session = Depends(get_db),
             current_user:User=Depends(get_current_active_user)
             ):
    account = db.query(Account).filter(Account.id == transaction_amt.from_account_id,
                                       Account.user_id == current_user.id
                                       ).first()
    if not account:
        HTTPException(status_code=404, detail="Account not found")
    if transaction_amt.amount > account.balance:
        raise HTTPException(status_code=400,
                            detail="Amount should be less than available balance{account.balance}")
    
    account.balance -= transaction_amt.amount

    transaction_withdraw = Transaction(from_account_id = account.id,
                              type="withdraw",
                              amount = transaction_amt.amount,
                              timestamp= datetime.utcnow()
                    )
    
    db.add(transaction_withdraw)
    db.commit()
    db.refresh(transaction_withdraw)
    return transaction_withdraw

#####
@router.post("/transfer",response_model= TransactionOut)
def transfer(account_details:TransactionCreate,
             db:Session = Depends(get_db),
             user:User = Depends(get_current_active_user)):
    
    from_account = db.query(Account).filter(
        Account.id == account_details.from_account_id,
        Account.user_id == user.id
    ).first()
    if not from_account:
        raise HTTPException(status_code= 404,
                            detail = "from_account is not found")
    to_account = db.query(Account).filter(
        Account.id == account_details.to_account_id,
        Account.user_id == user.id
    ).first()

    if not to_account:
        raise HTTPException(status_code=404,
                            detail = "to_account not found")
    
    if from_account.balance < account_details.amount:
        raise HTTPException(status_code=400,
                            detail = "Insufficient balance"
                            )

    from_account.balance -=  account_details.amount
    to_account.balance += account_details.amount

    transfer_amount = Transaction(from_account_id = from_account.id,
                                  to_account_id = to_account.id,
                                  type = 'transfer',
                                  timestamp = datetime.utcnow()
                                  )
    
    db.add(transfer_amount)
    db.commit()
    db.refresh(transfer_amount)
    return transfer_amount
#####  

@router.get("/{account_id}/history", response_model=List[TransactionOut])
def transaction_history(account_id: int,
                        current_user: User = Depends(get_current_active_user),
                        db: Session = Depends(get_db)):

    account = db.query(Account).filter(
        Account.user_id == current_user.id,
        Account.id == account_id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    transactions = db.query(Transaction).filter(
        (Transaction.to_account_id == account.id) |
        (Transaction.from_account_id == account.id)
    ).order_by(Transaction.timestamp.desc()).all()

    # Validate each transaction
    for each_trns in transactions:
        if each_trns.from_account_id is None:
            logger.error(f"Invalid transaction: {each_trns.id} has from_account_id = None")
            raise HTTPException(
                status_code=5001,
                detail=f"Transaction {each_trns.id} has invalid from_account_id"
            )

    logger.debug(f"Transaction history for account {account_id}: {[txn.id for txn in transactions]}")

    return transactions