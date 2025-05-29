# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import accounts, transactions, brokerage, chat

app = FastAPI(title="Bank Buddy API")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Existing routers
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(brokerage.router)

# New router for chatbot
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Welcome to Bank Buddy API"}
