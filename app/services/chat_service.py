
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.banking import ChatSession, ChatMessage


def create_chat_session(db: Session, customer_id: int):
    session = ChatSession(customer_id=customer_id)

    db.add(session)
    db.flush()

    return session


def get_owned_session(
    db: Session,
    session_id: int,
    customer_id: int
):
    session = db.scalar(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.customer_id == customer_id
        )
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    return session


def save_message(
    db: Session,
    session_id: int,
    role: str,
    content: str
):
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)
    db.flush()

    return message


def get_customer_sessions(db: Session, customer_id: int):
    return db.scalars(
        select(ChatSession)
        .where(ChatSession.customer_id == customer_id)
        .order_by(ChatSession.id.desc())
    ).all()


def get_session_messages(db: Session, session_id: int):
    return db.scalars(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id.asc())
    ).all()
