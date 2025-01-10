from sqlalchemy.orm import Session
from app.models import Account, BrokerageHolding, Transaction
from datetime import datetime, timezone


# Use your real-time stock price function
from app.services.stock_service import get_realtime_price


def buy_stock(db: Session, brokerage_id: int, ticker: str, shares: float):
    """
    Buy 'shares' of 'ticker' in the given brokerage account.
    
    - Deduct the purchase cost from 'purchase_balance'.
    - Update or create a BrokerageHolding entry for this ticker.
    """
    # 1) Locate brokerage account
    brokerage_acct = db.query(Account).filter(
        Account.id == brokerage_id,
        Account.account_type == "brokerage"
    ).first()
    if not brokerage_acct:
        raise ValueError(f"Brokerage account {brokerage_id} not found.")

    # 2) Get current stock price
    current_price = get_realtime_price(ticker)
    total_cost = current_price * shares

    # 3) Ensure there's enough in 'purchase_balance'
    if brokerage_acct.purchase_balance < total_cost:
        raise ValueError("Insufficient purchase_balance to buy stock.")

    # Deduct from purchase_balance
    brokerage_acct.purchase_balance -= total_cost

    # 4) Check if there's already a holding for this ticker
    holding = db.query(BrokerageHolding).filter(
        BrokerageHolding.brokerage_account_id == brokerage_acct.id,
        BrokerageHolding.ticker == ticker
    ).first()

    # Update or create the holding
    if holding:
        old_shares = holding.shares
        new_shares = old_shares + shares
        # Weighted average cost
        holding.avg_cost = (
            (holding.avg_cost * old_shares) + (current_price * shares)
        ) / new_shares
        holding.shares = new_shares
    else:
        holding = BrokerageHolding(
            brokerage_account_id=brokerage_acct.id,
            ticker=ticker,
            shares=shares,
            avg_cost=current_price
        )
        db.add(holding)

    # 5) Record a transaction
    tx = Transaction(
        account_id=brokerage_acct.id,
        date=datetime.now(timezone.utc),
        description=f"Buy {shares} share(s) of {ticker} @ {current_price}",
        type="PURCHASE",
        amount=-total_cost,
        running_balance=brokerage_acct.purchase_balance,  # Reflecting how much is left in purchase_balance
    )
    db.add(tx)

    # 6) Commit
    db.commit()
    db.refresh(brokerage_acct)
    db.refresh(holding)


def sell_stock(db: Session, brokerage_id: int, ticker: str, shares: float):
    """
    Sell 'shares' of 'ticker' from the given brokerage account.
    
    - Add proceeds to 'purchase_balance'.
    - Update the BrokerageHolding entry.
    """
    # 1) Locate brokerage account
    brokerage_acct = db.query(Account).filter(
        Account.id == brokerage_id,
        Account.account_type == "brokerage"
    ).first()
    if not brokerage_acct:
        raise ValueError(f"Brokerage account {brokerage_id} not found.")

    # 2) Find the holding
    holding = db.query(BrokerageHolding).filter(
        BrokerageHolding.brokerage_account_id == brokerage_acct.id,
        BrokerageHolding.ticker == ticker
    ).first()
    if not holding or holding.shares < shares:
        raise ValueError("Not enough shares to sell.")

    # 3) Get current price and compute proceeds
    current_price = get_realtime_price(ticker)
    proceeds = current_price * shares

    # 4) Update holding
    holding.shares -= shares
    if holding.shares <= 0:
        # Optionally remove the holding if zero shares left
        db.delete(holding)

    # 5) Add proceeds to 'purchase_balance'
    brokerage_acct.purchase_balance += proceeds

    # 6) Record a transaction
    tx = Transaction(
        account_id=brokerage_acct.id,
        date=datetime.now(timezone.utc),
        description=f"Sell {shares} share(s) of {ticker} @ {current_price}",
        type="SELL",
        amount=proceeds,
        running_balance=brokerage_acct.purchase_balance
    )
    db.add(tx)

    db.commit()
    db.refresh(brokerage_acct)


def transfer_funds(db: Session, from_account_name: str, to_account_name: str, amount: float):
    """
    Transfer 'amount' from one account to another.
    - If transferring *to* a brokerage, we place it in 'purchase_balance'.
    - If transferring *from* a brokerage, we deduct from 'purchase_balance'.
    - For normal accounts (checking/savings/credit_card), use 'balance'.
    """
    from_acct = db.query(Account).filter(
        Account.account_name.ilike(f"%{from_account_name}%")
    ).first()
    if not from_acct:
        raise ValueError(f"From-account '{from_account_name}' not found.")

    to_acct = db.query(Account).filter(
        Account.account_name.ilike(f"%{to_account_name}%")
    ).first()
    if not to_acct:
        raise ValueError(f"To-account '{to_account_name}' not found.")

    # 1) Check 'from_account' for sufficient funds
    if from_acct.account_type.lower() == "brokerage":
        if from_acct.purchase_balance < amount:
            raise ValueError("Insufficient purchase_balance in from_account.")
        from_acct.purchase_balance -= amount
    else:
        if from_acct.balance < amount:
            raise ValueError("Insufficient funds in from_account.")
        from_acct.balance -= amount

    # 2) Deposit into 'to_account'
    if to_acct.account_type.lower() == "brokerage":
        to_acct.purchase_balance += amount
    else:
        to_acct.balance += amount

    # 3) Record transaction for from_acct
    from_tx = Transaction(
        account_id=from_acct.id,
        date=datetime.now(timezone.utc),
        description=f"Transfer to {to_acct.account_name}",
        type="WITHDRAWAL",
        amount=-amount,
        running_balance=(from_acct.purchase_balance if from_acct.account_type.lower() == "brokerage"
                         else from_acct.balance)
    )
    db.add(from_tx)

    # 4) Record transaction for to_acct
    to_tx = Transaction(
        account_id=to_acct.id,
        date=datetime.now(timezone.utc),
        description=f"Transfer from {from_acct.account_name}",
        type="DEPOSIT",
        amount=amount,
        running_balance=(to_acct.purchase_balance if to_acct.account_type.lower() == "brokerage"
                         else to_acct.balance)
    )
    db.add(to_tx)

    db.commit()
    db.refresh(from_acct)
    db.refresh(to_acct)


def pay_credit_card(db: Session, from_account_name: str, credit_card_account_name: str, amount: float):
    """
    Pay 'amount' from one account to a credit card.
    - Deduct from from_acct (balance or purchase_balance if it's brokerage).
    - Decrease the credit card's 'balance' by that amount.
    - No transaction records are created, only direct balance updates.
    """
    from_acct = db.query(Account).filter(
        Account.account_name.ilike(f"%{from_account_name}%")
    ).first()
    if not from_acct:
        raise ValueError(f"From-account '{from_account_name}' not found.")

    credit_card_acct = db.query(Account).filter(
        Account.account_name.ilike(f"%{credit_card_account_name}%"),
        Account.account_type == "credit_card"
    ).first()
    if not credit_card_acct:
        raise ValueError(f"Credit card account '{credit_card_account_name}' not found.")

    # Deduct from from_acct
    if from_acct.account_type.lower() == "brokerage":
        if from_acct.purchase_balance < amount:
            raise ValueError("Insufficient purchase_balance for credit card payment.")
        from_acct.purchase_balance -= amount
    else:
        if from_acct.balance < amount:
            raise ValueError("Insufficient funds for credit card payment.")
        from_acct.balance -= amount

    # Decrease the credit card's balance
    credit_card_acct.balance -= amount
    if credit_card_acct.balance < 0:
        credit_card_acct.balance = 0  # Or allow negative if you want to track overpayment

    db.commit()
    db.refresh(from_acct)
    db.refresh(credit_card_acct)

def get_account_balance(db: Session, account_name: str) -> float:
    """
    Return the current 'balance' for the given account name. 
    If the account is brokerage, optionally add purchase_balance to reflect total cash on hand.
    """
    acct = db.query(Account).filter(
        Account.account_name.ilike(f"%{account_name}%")
    ).first()
    if not acct:
        raise ValueError(f"Account '{account_name}' not found.")

    if acct.account_type.lower() == "brokerage":
        # Combine both to show total funds in brokerage
        return acct.balance + acct.purchase_balance
    else:
        return acct.balance
    
def get_brokerage_value(db: Session, brokerage_id: int) -> float:
    """
    Return the total current portfolio value for the given brokerage account,
    summing:
      - purchase_balance (cash available to buy stocks)
      - (optionally) balance, if you want to track any leftover funds
      - the sum of each holding's market value (shares * current price).
    """
    brokerage_acct = db.query(Account).filter(
        Account.id == brokerage_id,
        Account.account_type == "brokerage"
    ).first()
    if not brokerage_acct:
        raise ValueError(f"Brokerage account {brokerage_id} not found.")

    # Start with any leftover 'balance' plus 'purchase_balance'
    total_value = brokerage_acct.balance + brokerage_acct.purchase_balance

    # Now add the market value of each holding
    holdings = db.query(BrokerageHolding).filter(
        BrokerageHolding.brokerage_account_id == brokerage_acct.id
    ).all()
    for holding in holdings:
        current_price = get_realtime_price(holding.ticker)
        total_value += current_price * holding.shares

    return round(total_value, 2)
