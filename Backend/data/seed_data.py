import os
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app import models
from datetime import datetime, timedelta, timezone

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()
    try:
        # 1. Create a user: Middle-class man John Doe
        john = models.User(
            name="John Doe",
            email="john.doe@example.com",
            phone="555-987-6543"
        )
        db.add(john)
        db.commit()
        db.refresh(john)

        # 2. Create accounts linked to John Doe
        checking = models.Account(
            user_id=john.id,
            account_type="checking",
            account_name="MyBank Checking",
            account_num="CHK123456789",
            routing_num="111000025",
            balance=3500.75
        )

        savings = models.Account(
            user_id=john.id,
            account_type="savings",
            account_name="MyBank Savings",
            account_num="SVG987654321",
            routing_num="111000025",
            balance=8400.50
        )

        credit_card = models.Account(
            user_id=john.id,
            account_type="credit_card",
            account_name="MyBank Visa",
            account_num="4111111111111111",
            routing_num=None,
            credit_limit=5000.00,
            apr=15.99,
            balance=1200.45  # Current outstanding balance
        )

        brokerage = models.Account(
            user_id=john.id,
            account_type="brokerage",
            account_name="MyBrokerage",
            account_num="BRK123456",
            routing_num=None,
            balance=7700.00, # Representing total portfolio value
            purchase_balance=0.00
        )

        db.add_all([checking, savings, credit_card, brokerage])
        db.commit()

        # Refresh accounts to get their IDs
        db.refresh(checking)
        db.refresh(savings)
        db.refresh(credit_card)
        db.refresh(brokerage)

        # 3. Create brokerage holdings for John
        holdings = [
            models.BrokerageHolding(
                brokerage_account_id=brokerage.id,
                ticker="AAPL",
                shares=10,
                avg_cost=140.00
            ),
            models.BrokerageHolding(
                brokerage_account_id=brokerage.id,
                ticker="TSLA",
                shares=5,
                avg_cost=650.00
            ),
            models.BrokerageHolding(
                brokerage_account_id=brokerage.id,
                ticker="MSFT",
                shares=8,
                avg_cost=250.00
            )
        ]
        db.add_all(holdings)
        db.commit()

        # 4. Create fake transactions for checking account (only purchases and deposits)
        checking_transactions = [
            {
                "date": datetime.now(timezone.utc) - timedelta(days=30),
                "description": "Paycheck Deposit",
                "type": "DEPOSIT",
                "amount": 2000.00,
                "running_balance": 5500.75  # 3500.75 + 2000
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=28),
                "description": "Grocery Store Purchase",
                "type": "PURCHASE",
                "amount": -150.25,
                "running_balance": 5350.50
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=25),
                "description": "Utility Bill Payment",
                "type": "PURCHASE",
                "amount": -120.00,
                "running_balance": 5230.50
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=22),
                "description": "Restaurant Dinner",
                "type": "PURCHASE",
                "amount": -75.50,
                "running_balance": 5155.00
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=20),
                "description": "Online Shopping - Amazon",
                "type": "PURCHASE",
                "amount": -220.80,
                "running_balance": 4934.20
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=18),
                "description": "Gym Membership",
                "type": "PURCHASE",
                "amount": -45.00,
                "running_balance": 4889.20
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=15),
                "description": "Car Maintenance",
                "type": "PURCHASE",
                "amount": -350.00,
                "running_balance": 4539.20
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=12),
                "description": "Gas Station",
                "type": "PURCHASE",
                "amount": -60.75,
                "running_balance": 4478.45
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=10),
                "description": "Coffee Shop",
                "type": "PURCHASE",
                "amount": -15.50,
                "running_balance": 4462.95
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=7),
                "description": "Movie Theater",
                "type": "PURCHASE",
                "amount": -40.00,
                "running_balance": 4422.95
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=5),
                "description": "Electronics Store",
                "type": "PURCHASE",
                "amount": -500.00,
                "running_balance": 3922.95
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=2),
                "description": "Bookstore",
                "type": "PURCHASE",
                "amount": -30.25,
                "running_balance": 3892.70
            }
        ]

        # 5. Create fake transactions for credit card (only purchases)
        credit_card_transactions = [
            {
                "date": datetime.now(timezone.utc) - timedelta(days=29),
                "description": "Amazon Purchase",
                "type": "PURCHASE",
                "amount": 65.80,
                "running_balance": 65.80
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=27),
                "description": "Gas Station",
                "type": "PURCHASE",
                "amount": 40.00,
                "running_balance": 105.80
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=24),
                "description": "Restaurant Dinner",
                "type": "PURCHASE",
                "amount": 75.50,
                "running_balance": 181.30
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=21),
                "description": "Online Shopping - eBay",
                "type": "PURCHASE",
                "amount": 120.45,
                "running_balance": 301.75
            },
            {
                "date": datetime.utcnow() - timedelta(days=19),
                "description": "Gym Membership",
                "type": "PURCHASE",
                "amount": 45.00,
                "running_balance": 346.75
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=16),
                "description": "Car Maintenance",
                "type": "PURCHASE",
                "amount": 350.00,
                "running_balance": 696.75
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=14),
                "description": "Electronics Store",
                "type": "PURCHASE",
                "amount": 500.00,
                "running_balance": 1196.75
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=12),
                "description": "Bookstore",
                "type": "PURCHASE",
                "amount": 30.25,
                "running_balance": 1227.00
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=10),
                "description": "Travel Booking",
                "type": "PURCHASE",
                "amount": 200.00,
                "running_balance": 1427.00
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=8),
                "description": "Coffee Shop",
                "type": "PURCHASE",
                "amount": 20.50,
                "running_balance": 1447.50
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=5),
                "description": "Movie Theater",
                "type": "PURCHASE",
                "amount": 40.00,
                "running_balance": 1487.50
            },
            {
                "date": datetime.now(timezone.utc) - timedelta(days=3),
                "description": "Clothing Store",
                "type": "PURCHASE",
                "amount": 150.00,
                "running_balance": 1637.50
            }
        ]

        # 6. Add checking transactions to the session
        for tx in checking_transactions:
            transaction = models.Transaction(
                account_id=checking.id,
                date=tx["date"],
                description=tx["description"],
                type=tx["type"],
                amount=tx["amount"],
                running_balance=tx["running_balance"]
            )
            db.add(transaction)

        # 7. Add credit card transactions to the session
        for tx in credit_card_transactions:
            transaction = models.Transaction(
                account_id=credit_card.id,
                date=tx["date"],
                description=tx["description"],
                type=tx["type"],
                amount=tx["amount"],
                running_balance=tx["running_balance"]
            )
            db.add(transaction)

        db.commit()
        print("Database seeded successfully.")

    except Exception as e:
        db.rollback()
        print("Error seeding data:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
