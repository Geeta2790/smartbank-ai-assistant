
from app.agents.state import BankingState
from app.services.banking_service import fetch_transactions


def transaction_agent(state: BankingState) -> dict:
    customer_id = state["customer_id"]

    transactions = fetch_transactions(customer_id)

    if not transactions:
        return {
            "response": "No transactions were found."
        }

    lines = []

    for tx in transactions:
        lines.append(
            f"{tx['type'].title()}: "
            f"₹{tx['amount']} - {tx['description']}"
        )

    return {"response": "\n".join(lines)}
