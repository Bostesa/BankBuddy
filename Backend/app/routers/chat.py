import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Account  # Add this line to import the Account model
from app.services.llm_service import generate_text
from app.services.financial_logic import (
    buy_stock,
    sell_stock,
    transfer_funds,
    pay_credit_card,
    get_account_balance,
    get_brokerage_value,
    get_user_stocks,
)

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    stream: Optional[bool] = False

def get_db():
    """
    Dependency that yields a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def handle_chat(req: ChatRequest, db: Session = Depends(get_db)):
    user_prompt = req.message

    # 1) First LLM call: interpret user's request
    llm_raw_output = generate_text(user_prompt)

    # 2) Clean Markdown formatting and parse JSON
    try:
        cleaned_output = llm_raw_output.strip()
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output.replace("```json", "").strip()
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output.rsplit("```", 1)[0].strip()

        llm_data = json.loads(cleaned_output)
        intent = llm_data.get("intent")
        params = llm_data.get("parameters", {})
    except json.JSONDecodeError:
        return {"reply": "Sorry, I couldn't understand that request."}

    if not intent:
        return {"reply": "I didn't understand your request."}

    final_text = ""

    # 3) Execute financial operations based on intent
    try:
        if intent == "GET_HOLDINGS":
            user_id = 1  # Assuming single user scenario; adjust as needed
            # Optionally update brokerage value before retrieving holdings
            brokerage_account = db.query(Account).filter_by(user_id=user_id, account_type="brokerage").first()
            if brokerage_account:
                stocks = get_user_stocks(db, user_id)
                if not stocks:
                    final_text = "You have no stock holdings at the moment."
                else:
                    lines = []
                    for stk in stocks:
                        lines.append(f"{stk['ticker']}: {stk['shares']} shares at avg cost ${stk['avg_cost']}")
                    final_text = "Your stock portfolio has been updated! Here's a summary of your holdings:\n" + "\n".join(lines)
        elif intent == "BUY_STOCK":
            ticker = params.get("ticker")
            shares = params.get("shares")
            if not all([ticker, shares]):
                final_text = "Failed to buy stock: Missing ticker or share quantity."
            else:
                brokerage_account = db.query(Account).filter_by(account_type="brokerage").first()
                if not brokerage_account:
                    final_text = "No brokerage account found."
                else:
                    buy_stock(db, brokerage_account.id, str(ticker), float(shares))
                    final_text = f"Bought {shares} shares of {ticker}."

        elif intent == "SELL_STOCK":
            ticker = params.get("ticker")
            shares = params.get("shares")
            if not all([ticker, shares]):
                final_text = "Failed to sell stock: Missing ticker or share quantity."
            else:
                brokerage_account = db.query(Account).filter_by(account_type="brokerage").first()
                if not brokerage_account:
                    final_text = "No brokerage account found."
                else:
                    sell_stock(db, brokerage_account.id, str(ticker), float(shares))
                    final_text = f"Sold {shares} shares of {ticker}."

        elif intent == "TRANSFER_FUNDS":
            from_acct = params.get("from_account")
            to_acct = params.get("to_account")
            amount = params.get("amount")
            if not all([from_acct, to_acct, amount]):
                final_text = "Failed to transfer funds: Missing parameters."
            else:
                transfer_funds(db, from_acct, to_acct, float(amount))
                final_text = f"Transferred ${amount} from {from_acct} to {to_acct}."

        elif intent == "PAY_CREDIT_CARD":
            from_acct = params.get("from_account")
            amount = params.get("amount")
            if not all([from_acct, amount]):
                final_text = "Failed to pay credit card: Missing from_account or amount."
            else:
                credit_card_account = db.query(Account).filter_by(account_type="credit_card").first()
                if not credit_card_account:
                    final_text = "No credit card account found."
                else:
                    pay_credit_card(db, from_acct, credit_card_account.account_name, float(amount))
                    final_text = f"Paid ${amount} toward credit card {credit_card_account.account_name} from {from_acct}."

        elif intent == "GET_ACCOUNT_BALANCE":
            account_type = params.get("account_type")
            if not account_type:
                final_text = "Failed to check balance: Missing account type."
            else:
                if account_type.lower().replace(" ", "") == "creditcard":
                    account_type = "MyBank Visa"  # The actual name in your DB
                balance_value = get_account_balance(db, account_type)
                final_text = f"Your {account_type} account balance is ${balance_value}."

        elif intent == "GET_BROKERAGE_VALUE":
            brokerage_account = db.query(Account).filter_by(account_type="brokerage").first()
            if not brokerage_account:
                final_text = "No brokerage account found."
            else:
                total_value = get_brokerage_value(db, brokerage_account.id)
                final_text = f"Your brokerage account value is ${total_value}."

        else:
            final_text = f"Unhandled intent: {intent}."
    except Exception as e:
        final_text = f"An error occurred during the operation: {str(e)}"

    # 4) Request a user-friendly message from the LLM
    confirmation_prompt = f"""
    A financial operation was just performed, summarized as:
    '{final_text}'

    Please produce a concise, friendly message for the user.
    """
    friendly_message = generate_text(confirmation_prompt)

    try:
        cleaned_friendly = friendly_message.strip()
        if cleaned_friendly.startswith("```json"):
            cleaned_friendly = cleaned_friendly.replace("```json", "").strip()
        if cleaned_friendly.endswith("```"):
            cleaned_friendly = cleaned_friendly.rsplit("```", 1)[0].strip()
    except Exception:
        cleaned_friendly = friendly_message

    return {"reply": cleaned_friendly}
