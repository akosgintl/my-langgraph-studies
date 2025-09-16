"""LangChain v1 agent + MCP HTTP itinerary server example.

Prerequisite:
  Start the local MCP server defined in `mcp_server_basic.py` on port 8000:
      python examples/mcp_server_basic.py
"""
import asyncio
import logging
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from rich.logging import RichHandler

logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("lang_itinerary")

load_dotenv(override=True)
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


async def run_agent():
    client = MultiServerMCPClient(
        {
            "itinerary": {
                # Make sure you start your itinerary server on port 8000
                "url": "http://localhost:8000/mcp/",
                "transport": "streamable_http",
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(model, tools)

    user_query = (
        "Find me a hotel in San Francisco for 2 nights starting from 2026-01-01. "
        "I need a hotel with free WiFi and a pool."
    )

    response = await agent.ainvoke({"messages": [HumanMessage(content=user_query)]})
    final = response["messages"][-1].content
    print(final)


def main():
    asyncio.run(run_agent())


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    main()
