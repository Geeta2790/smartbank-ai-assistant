
from app.agents.state import BankingState
from app.services.banking_service import fetch_loans


def loan_agent(state: BankingState) -> dict:
    customer_id = state["customer_id"]

    loans = fetch_loans(customer_id)

    if not loans:
        return {"response": "No loans were found."}

    lines = []

    for loan in loans:
        lines.append(
            f"{loan['loan_type']}: "
            f"Outstanding ₹{loan['outstanding_amount']}, "
            f"EMI ₹{loan['emi_amount']}"
        )

    return {"response": "\n".join(lines)}
