
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.banking import Account, Loan, Transaction


def fetch_balance(customer_id: int):
    with SessionLocal() as db:
        account = db.scalar(
            select(Account).where(
                Account.customer_id == customer_id
            ).order_by(Account.id)
        )

        if account is None:
            return None

        return {
            "account_type": account.account_type,
            "balance": str(account.balance)
        }


def fetch_loans(customer_id: int):
    with SessionLocal() as db:
        loans = db.scalars(
            select(Loan).where(
                Loan.customer_id == customer_id
            ).order_by(Loan.id)
        ).all()

        return [
            {
                "loan_type": loan.loan_type,
                "outstanding_amount": str(loan.outstanding_amount),
                "emi_amount": str(loan.emi_amount)
            }
            for loan in loans
        ]


def fetch_transactions(customer_id: int):
    with SessionLocal() as db:
        account_ids = select(Account.id).where(
            Account.customer_id == customer_id
        )

        transactions = db.scalars(
            select(Transaction)
            .where(Transaction.account_id.in_(account_ids))
            .order_by(
                Transaction.created_at.desc(),
                Transaction.id.desc()
            )
            .limit(5)
        ).all()

        return [
            {
                "amount": str(tx.amount),
                "type": tx.transaction_type,
                "description": tx.description
            }
            for tx in transactions
        ]
