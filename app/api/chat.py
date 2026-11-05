
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.banking import Customer
from app.security.dependencies import get_current_customer
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    SessionResponse,
    HistoryResponse,
    MessageResponse,
)
from app.services.chat_service import (
    create_chat_session,
    get_owned_session,
    save_message,
    get_customer_sessions,
    get_session_messages,
)
from app.agents.graph import graph

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    try:
        if request.session_id is None:
            session = create_chat_session(db, customer.id)
        else:
            session = get_owned_session(
                db, request.session_id, customer.id
            )

        result = await graph.ainvoke({
            "question": request.question,
            "customer_id": customer.id,
            "intent": "",
            "response": "",
        })

        answer = result["response"]
        intent = result["intent"]

        save_message(
            db, session.id, "user", request.question
        )
        save_message(
            db, session.id, "assistant", answer
        )

        response = ChatResponse(
            session_id=session.id,
            intent=intent,
            answer=answer,
        )

        db.commit()
        return response

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to process chat request"
        )


@router.get("/history", response_model=list[SessionResponse])
def list_history(
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    sessions = get_customer_sessions(db, customer.id)

    return [
        SessionResponse(
            session_id=session.id,
            created_at=session.created_at,
        )
        for session in sessions
    ]


@router.get(
    "/history/{session_id}",
    response_model=HistoryResponse,
)
def get_history(
    session_id: int,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    get_owned_session(db, session_id, customer.id)

    messages = get_session_messages(db, session_id)

    return HistoryResponse(
        session_id=session_id,
        messages=[
            MessageResponse(
                id=message.id,
                role=message.role,
                content=message.content,
            )
            for message in messages
        ],
    )
