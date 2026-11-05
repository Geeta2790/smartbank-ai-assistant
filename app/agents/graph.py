
from langgraph.graph import StateGraph, START, END

from app.agents.state import BankingState
from app.agents.orchestrator import orchestrator, route_agent
from app.agents.banking_agent import banking_agent
from app.agents.loan_agent import loan_agent
from app.agents.transaction_agent import transaction_agent


def unsupported_agent(state: BankingState) -> dict:
    return {
        "response": (
            "I can help with bank balances, "
            "loans, EMIs and recent transactions."
        )
    }


builder = StateGraph(BankingState)

# 1. Register nodes
builder.add_node("orchestrator", orchestrator)
builder.add_node("banking", banking_agent)
builder.add_node("loan", loan_agent)
builder.add_node("transaction", transaction_agent)
builder.add_node("unsupported", unsupported_agent)

# 2. Start with orchestrator
builder.add_edge(START, "orchestrator")

# 3. Dynamically select specialist agent
builder.add_conditional_edges(
    "orchestrator",
    route_agent,
    {
        "banking": "banking",
        "loan": "loan",
        "transaction": "transaction",
        "unsupported": "unsupported"
    }
)

# 4. End after specialist returns
builder.add_edge("banking", END)
builder.add_edge("loan", END)
builder.add_edge("transaction", END)
builder.add_edge("unsupported", END)

# 5. Compile workflow
graph = builder.compile()
