# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    accounts = relationship("Account", backref="user")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_type = Column(String)      # e.g. "checking", "savings", "credit_card", "brokerage"
    account_name = Column(String)
    account_num = Column(String)
    routing_num = Column(String, nullable=True)
    credit_limit = Column(Float, nullable=True)
    apr = Column(Float, nullable=True)
    balance = Column(Float, default=0.0)          # current cash balance
    purchase_balance = Column(Float, default=0.0) # new field for funds allocated for purchases
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    transactions = relationship("Transaction", backref="account")
    holdings = relationship("BrokerageHolding", backref="brokerage_account", lazy="dynamic")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    date = Column(DateTime, default=datetime.now(timezone.utc))
    description = Column(String)
    type = Column(String)  # "DEPOSIT", "WITHDRAWAL", "PURCHASE", etc.
    amount = Column(Float)
    running_balance = Column(Float)

class BrokerageHolding(Base):
    __tablename__ = "brokerage_holdings"
    id = Column(Integer, primary_key=True, index=True)
    brokerage_account_id = Column(Integer, ForeignKey("accounts.id"))
    ticker = Column(String)
    shares = Column(Float)
    avg_cost = Column(Float)
