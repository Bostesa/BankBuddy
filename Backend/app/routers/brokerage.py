# app/routers/brokerage.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.dependencies import get_db
from app.services import stock_service

router = APIRouter(prefix="/brokerage", tags=["Brokerage"])

@router.get("/{brokerage_id}", summary="Get brokerage account details")
def get_brokerage_account(brokerage_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(
        models.Account.id == brokerage_id,
        models.Account.account_type == "brokerage"
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Brokerage account not found")
    holdings = db.query(models.BrokerageHolding).filter(
        models.BrokerageHolding.brokerage_account_id == account.id
    ).all()
    return {"account": account, "holdings": holdings}

@router.post("/buy/{brokerage_id}", summary="Buy shares using brokerage account")
def buy_shares(brokerage_id: int, ticker: str, shares: float, db: Session = Depends(get_db)):
    # Retrieve brokerage account
    brokerage = db.query(models.Account).filter(
        models.Account.id == brokerage_id,
        models.Account.account_type == "brokerage"
    ).first()
    if not brokerage:
        raise HTTPException(status_code=404, detail="Brokerage account not found")

    # Get current stock price
    try:
        current_price = stock_service.get_realtime_price(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    total_cost = current_price * shares

    # Check if user has enough funds (assuming brokerage.balance is available cash)
    if brokerage.balance < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient funds to buy shares")

    # Deduct funds
    brokerage.balance -= total_cost

    # Update or create holding
    holding = db.query(models.BrokerageHolding).filter(
        models.BrokerageHolding.brokerage_account_id == brokerage.id,
        models.BrokerageHolding.ticker == ticker
    ).first()

    if holding:
        # Update existing holding
        total_shares = holding.shares + shares
        # Assume avg_cost recalculates (simple weighted average)
        holding.avg_cost = ((holding.avg_cost * holding.shares) + (current_price * shares)) / total_shares
        holding.shares = total_shares
    else:
        # Create a new holding
        holding = models.BrokerageHolding(
            brokerage_account_id=brokerage.id,
            ticker=ticker,
            shares=shares,
            avg_cost=current_price
        )
        db.add(holding)

    db.commit()
    db.refresh(brokerage)
    return {
        "message": f"Purchased {shares} shares of {ticker} at ${current_price:.2f} each.",
        "new_balance": brokerage.balance
    }
