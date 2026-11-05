from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.banking import Account, Loan, Transaction

router = APIRouter(
    prefix="/banking",
    tags=["Banking"]
)


@router.get("/balance/{customer_id}")
def get_balance(
    customer_id: int,
    db: Session = Depends(get_db)
):
    account = db.scalar(
        select(Account).where(
            Account.customer_id == customer_id
        )
    )

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "account_id": account.id,
        "account_type": account.account_type,
        "balance": str(account.balance)
    }


@router.get("/loans/{customer_id}")
def get_loans(
    customer_id: int,
    db: Session = Depends(get_db)
):
    loans = db.scalars(
        select(Loan).where(
            Loan.customer_id == customer_id
        )
    ).all()

    return [
        {
            "loan_id": loan.id,
            "loan_type": loan.loan_type,
            "outstanding_amount": str(loan.outstanding_amount),
            "emi_amount": str(loan.emi_amount)
        }
        for loan in loans
    ]


@router.get("/transactions/{customer_id}")
def get_transactions(
    customer_id: int,
    db: Session = Depends(get_db)
):
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
            "transaction_id": transaction.id,
            "amount": str(transaction.amount),
            "type": transaction.transaction_type,
            "description": transaction.description
        }
        for transaction in transactions
    ]