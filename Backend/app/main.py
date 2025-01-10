# app/main.py

from fastapi import FastAPI
from app.routers import accounts, transactions, brokerage, chat

app = FastAPI(title="Bank Buddy API")

# Existing routers
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(brokerage.router)

# New router for chatbot
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Welcome to Bank Buddy API"}
