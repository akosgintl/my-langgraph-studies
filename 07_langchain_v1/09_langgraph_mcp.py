"""Custom LangGraph state graph + MCP HTTP example.

Prerequisite:
Start the local MCP server defined in `mcp_server_basic.py` on port 8000:
    python examples/mcp_server_basic.py or python examples/mcp_server_basic.py --mcp-host localhost --mcp-port 8000
"""

import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

# Setup the client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


async def setup_agent():
    client = MultiServerMCPClient(
        {
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/mcp/",
                "transport": "streamable_http",
            }
        }
    )
    tools = await client.get_tools()

    def call_model(state: MessagesState):
        response = model.bind_tools(tools).invoke(state["messages"])
        return {"messages": response}

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    hotel_response = await graph.ainvoke(
        {"messages": "Find a hotel in SF for 2 nights starting from 2024-01-01. I need free WiFi and pool."}
    )
    print(hotel_response["messages"][-1].content)


if __name__ == "__main__":
    import asyncio
    import logging

    logging.basicConfig(level=logging.WARNING)
    asyncio.run(setup_agent())
