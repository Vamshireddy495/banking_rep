#Create/View bank account
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_current_active_user, get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse
from app.models.user import User
import logging
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

#Create Account API < Dependency injection is a software design pattern where objects (dependencies) are passed (injected) into a function or class rather than being created or fetched inside the function itself.>

@router.post("/",response_model= AccountResponse)
def create_account(account_data: AccountCreate,
                   db: Session = Depends(get_db),
                   current_user:User = Depends(get_current_active_user)
                ):
   
    account = Account(
        user_id = current_user.id,
        account_type = account_data.account_type,
        balance= account_data.initial_balance
        )
    
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


#Get all Accounts
@router.get("/",response_model= List[AccountResponse])
def get_all_accounts(db:Session = Depends(get_db),
                     current_user:User = Depends(get_current_active_user)):
    
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()

    return accounts

#Get single account
@router.get("/{account_id}",response_model = AccountResponse)
def get_account(account_id:int,
                db:Session = Depends(get_db),
                current_user:User= Depends(get_current_active_user)):
    
    account = db.query(Account).filter(Account.id == account_id,
                                       Account.user_id == current_user.id).first()
    
    
    if not account:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account Not found"
        )
    
    return account