from decimal import Decimal
from datetime import date, timedelta

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.banking import (
    Customer, Account, Transaction, Loan, LoanPayment
)


def seed_data():
    db = SessionLocal()

    try:
        existing = db.scalar(select(Customer.id).limit(1))

        if existing is not None:
            print("Customers already exist. Skipping seed.")
            return

        names = [
            "Rahul Sharma",
            "Priya Verma",
            "Amit Kumar",
            "Neha Singh",
            "Rohit Gupta"
        ]

        for index, name in enumerate(names, start=1):
            customer = Customer(
                name=name,
                email=f"demo{index}@example.com",
                password_hash="NOT_SET"
            )
            db.add(customer)
            db.flush()

            account = Account(
                customer_id=customer.id,
                account_type="Savings",
                balance=Decimal("85400.00") + Decimal(index * 1000)
            )
            db.add(account)
            db.flush()

            transactions = [
                Transaction(
                    account_id=account.id,
                    amount=Decimal("5000.00"),
                    transaction_type="credit",
                    description="Salary deposit"
                ),
                Transaction(
                    account_id=account.id,
                    amount=Decimal("1200.00"),
                    transaction_type="debit",
                    description="Shopping payment"
                )
            ]
            db.add_all(transactions)

            loan = Loan(
                customer_id=customer.id,
                loan_type="Personal Loan",
                outstanding_amount=Decimal("245000.00"),
                emi_amount=Decimal("8500.00")
            )
            db.add(loan)
            db.flush()

            payment = LoanPayment(
                loan_id=loan.id,
                amount=Decimal("8500.00"),
                due_date=date.today() + timedelta(days=15),
                status="pending"
            )
            db.add(payment)

        db.commit()
        print("Demo banking data inserted successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()