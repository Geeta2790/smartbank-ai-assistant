
import asyncio
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from mcp import Client

from app.mcp.server import mcp


class MCPState(TypedDict):
    question: str
    response: str


async def mcp_tool_node(state: MCPState):
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_supported_features",
            {}
        )

        if result.is_error:
            raise RuntimeError("MCP tool failed")

        features = result.structured_content or result.content

        return {"response": str(features)}


builder = StateGraph(MCPState)

builder.add_node("mcp_tool", mcp_tool_node)

builder.add_edge(START, "mcp_tool")
builder.add_edge("mcp_tool", END)

graph = builder.compile()


async def main():
    result = await graph.ainvoke({
        "question": "What can SmartBank do?",
        "response": ""
    })

    print(result["response"])


if __name__ == "__main__":
    asyncio.run(main())
