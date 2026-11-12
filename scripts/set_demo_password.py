from getpass import getpass

from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.banking import Customer
from app.security.auth import hash_password


with SessionLocal() as db:
    customer = db.scalar(
        select(Customer).where(
            Customer.email == "demo1@example.com"
        )
    )

    if customer is None:
        print("Demo customer not found")
    else:
        password = getpass("Enter a new demo password: ")

        if len(password) < 12:
            raise ValueError("Use at least 12 characters")

        customer.password_hash = hash_password(password)
        db.commit()

        print("Demo password updated successfully")