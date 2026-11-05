
import asyncio

from mcp import Client
from app.mcp.server import mcp


async def main():
    async with Client(mcp) as client:

        tools = await client.list_tools()

        print("Available MCP tools:")
        for tool in tools.tools:
            print("-", tool.name)

        result = await client.call_tool(
            "get_supported_features",
            {}
        )

        print("\nTool response:")
        print(result.structured_content or result.content)


if __name__ == "__main__":
    asyncio.run(main())
