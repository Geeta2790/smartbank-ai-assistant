
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.banking import Customer
from app.security.auth import decode_access_token

security = HTTPBearer(auto_error=False)


def get_current_customer(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db)
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise error

    try:
        payload = decode_access_token(credentials.credentials)
        customer_id = int(payload["sub"])
    except (ValueError, KeyError, Exception) as exc:
        raise error from exc

    customer = db.get(Customer, customer_id)

    if customer is None:
        raise error

    return customer
