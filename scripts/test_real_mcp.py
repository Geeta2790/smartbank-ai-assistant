
import asyncio

from app.agents.graph import graph


async def main():
    result = await graph.ainvoke({
        "question": "What is my bank balance?",
        "customer_id": 1,
        "intent": "",
        "response": ""
    })

    print("Agent:", result["intent"])
    print("Response:", result["response"])


if __name__ == "__main__":
    asyncio.run(main())
