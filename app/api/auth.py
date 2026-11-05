import hashlib
import hmac
import os
import secrets
import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.redis_client import redis_client
from app.models.banking import Customer
from app.security.auth import (
    verify_password,
    create_access_token,
    SECRET_KEY,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class OTPRequest(BaseModel):
    challenge_id: str
    otp: str = Field(pattern=r"^\d{6}$")


def otp_digest(challenge_id: str, otp: str) -> str:
    message = f"{challenge_id}:{otp}".encode()

    return hmac.new(
        SECRET_KEY.encode(),
        message,
        hashlib.sha256
    ).hexdigest()


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    customer = db.scalar(
        select(Customer).where(Customer.email == data.email)
    )

    if (
        customer is None
        or customer.password_hash == "NOT_SET"
        or not verify_password(data.password, customer.password_hash)
    ):
        raise HTTPException(401, "Invalid credentials")

    otp = f"{secrets.randbelow(1000000):06d}"
    challenge_id = secrets.token_urlsafe(24)

    redis_client.hset(
        f"otp:challenge:{challenge_id}",
        mapping={
            "customer_id": str(customer.id),
            "digest": otp_digest(challenge_id, otp),
            "attempts": "0"
        }
    )

    redis_client.expire(
        f"otp:challenge:{challenge_id}",
        300
    )

    # Local testing only. Never log OTPs in production.
    if os.getenv("LOCAL_OTP_DEBUG") == "true":
        print(f"LOCAL TEST OTP: {otp}")

    return {
        "message": "OTP challenge created",
        "challenge_id": challenge_id,
        "expires_in_seconds": 300
    }


# Atomically check, increment attempts, and consume a valid OTP.
VERIFY_OTP_SCRIPT = """
local key = KEYS[1]
local provided = ARGV[1]

if redis.call("EXISTS", key) == 0 then
    return {-1, ""}
end

local attempts = tonumber(redis.call("HGET", key, "attempts"))

if attempts >= 5 then
    redis.call("DEL", key)
    return {-2, ""}
end

local expected = redis.call("HGET", key, "digest")

if expected ~= provided then
    redis.call("HINCRBY", key, "attempts", 1)
    return {0, ""}
end

local customer_id = redis.call("HGET", key, "customer_id")
redis.call("DEL", key)

return {1, customer_id}
"""


@router.post("/verify-otp")
def verify_otp(data: OTPRequest):
    digest = otp_digest(data.challenge_id, data.otp)

    result = redis_client.eval(
        VERIFY_OTP_SCRIPT,
        1,
        f"otp:challenge:{data.challenge_id}",
        digest
    )

    status_code, customer_id = result

    if status_code != 1:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired OTP"
        )

    access_token = create_access_token(int(customer_id))

    logger.info("OTP verified successfully")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }