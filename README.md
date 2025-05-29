# BankBuddy

A full-stack personal finance assistant that lets you manage accounts and make financial transactions through a conversational chat interface.

## Features

- **Account Management**: View checking, savings, credit card, and brokerage accounts
- **Chat Interface**: Natural language commands for financial operations
- **Stock Trading**: Buy/sell stocks with real-time pricing
- **Fund Transfers**: Move money between accounts
- **Credit Card Payments**: Pay off credit card balances
- **Real-time Data**: Live stock prices via Alpha Vantage API

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, Tailwind CSS
- **AI**: Google Gemini for chat interpretation
- **Deployment**: Docker Compose

## Quick Start

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the application:
   ```bash
   docker compose up --build
   ```

3. Access the application at `http://localhost:3000`

## Sample Data

The app comes pre-seeded with a test user "John Doe" and multiple accounts for demonstration purposes.

## Chat Commands

Try natural language commands like:
- "Buy 10 shares of AAPL"
- "Transfer $500 from checking to savings"
- "Pay $200 on my credit card"
- "Show my portfolio"
