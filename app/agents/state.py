
from typing import TypedDict


class BankingState(TypedDict):
    question: str
    customer_id: int
    intent: str
    response: str
