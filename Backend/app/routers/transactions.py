# app/routers/transactions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.dependencies import get_db
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter(prefix="/transactions", tags=["Transactions"])

class TransactionCreate(BaseModel):
    description: str
    type: str
    amount: float

@router.get("/accounts/{account_id}", summary="Get transactions for an account")
def get_transactions(account_id: int, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).filter(models.Transaction.account_id == account_id).all()
    return transactions

@router.post("/accounts/{account_id}", summary="Create a transaction for an account")
def create_transaction(account_id: int, tx: TransactionCreate, db: Session = Depends(get_db)):
    # Fetch the account
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update the account balance based on transaction type
    # This is a basic implementation assuming PURCHASE reduces balance and DEPOSIT increases balance
    if tx.type.upper() == "PURCHASE":
        account.balance += tx.amount  # tx.amount should be negative for purchase
    elif tx.type.upper() == "DEPOSIT":
        account.balance += tx.amount

    # Create the transaction with current time in UTC
    new_tx = models.Transaction(
        account_id=account_id,
        date=datetime.now(timezone.utc),
        description=tx.description,
        type=tx.type,
        amount=tx.amount,
        running_balance=account.balance
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx
