
import asyncio

from mcp.server import MCPServer

from app.services.banking_service import (
    fetch_balance,
    fetch_loans,
    fetch_transactions,
)


def create_banking_mcp(customer_id: int):
    """
    Create an in-process MCP server for one
    authenticated customer.
    """
    mcp = MCPServer("SmartBank Tools")

    @mcp.tool()
    async def get_account_balance() -> dict:
        """Return the authenticated customer's balance."""
        account = await asyncio.to_thread(
            fetch_balance, customer_id
        )
        return account or {"message": "No account found"}

    @mcp.tool()
    async def get_loan_details() -> list[dict]:
        """Return the authenticated customer's loans."""
        return await asyncio.to_thread(
            fetch_loans, customer_id
        )

    @mcp.tool()
    async def get_recent_transactions() -> list[dict]:
        """Return the customer's last five transactions."""
        return await asyncio.to_thread(
            fetch_transactions, customer_id
        )

    return mcp
