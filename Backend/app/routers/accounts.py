# app/routers/accounts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.dependencies import get_db

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/", summary="Get all accounts for the user")
def get_all_accounts(db: Session = Depends(get_db)):
    # For a single user, just return all accounts
    accounts = db.query(models.Account).all()
    return accounts

@router.get("/{account_id}", summary="Get a specific account by ID")
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
