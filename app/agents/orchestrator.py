
from app.agents.state import BankingState


def orchestrator(state: BankingState) -> dict:
    question = state["question"].lower()

    if any(word in question for word in ["loan", "emi"]):
        intent = "loan"

    elif any(word in question for word in ["transaction", "spent", "statement"]):
        intent = "transaction"

    elif any(word in question for word in ["balance", "account"]):
        intent = "banking"

    else:
        intent = "unsupported"

    return {"intent": intent}


def route_agent(state: BankingState) -> str:
    return state["intent"]
