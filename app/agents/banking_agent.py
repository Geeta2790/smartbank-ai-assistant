
from mcp import Client

from app.agents.state import BankingState
from app.mcp.server import create_banking_mcp


async def banking_agent(state: BankingState) -> dict:
    customer_id = state["customer_id"]

    server = create_banking_mcp(customer_id)

    async with Client(server) as client:
        result = await client.call_tool(
            "get_account_balance",
            {}
        )

        if result.is_error:
            raise RuntimeError("Balance tool failed")

        data = result.structured_content

        if not data:
            return {"response": "Balance unavailable"}

        if "balance" not in data:
            return {
                "response": data.get(
                    "message", "No account found"
                )
            }

        return {
            "response": (
                f"Your {data['account_type']} account "
                f"balance is ₹{data['balance']}."
            )
        }
