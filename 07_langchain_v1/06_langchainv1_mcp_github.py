"""LangChain v1 MCP tools example (ported from LangGraph version).

This script demonstrates how to use LangChain v1 agent syntax with MCP tools
exposed by the GitHub MCP endpoint. It preserves the OpenAI vs GitHub
model selection logic from the original LangGraph based example.
"""

import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from rich import print
from rich.logging import RichHandler

logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("lang_triage")

load_dotenv(override=True)
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


class IssueProposal(BaseModel):
    """Contact information for a person."""

    url: str = Field(description="URL of the issue")
    title: str = Field(description="Title of the issue")
    summary: str = Field(description="Brief summary of the issue and signals for closing")
    should_close: bool = Field(description="Whether the issue should be closed or not")
    reply_message: str = Field(description="Message to post when closing the issue, if applicable")


async def main():
    mcp_client = MultiServerMCPClient(
        {
            "github": {
                "url": "https://api.githubcopilot.com/mcp/",
                "transport": "streamable_http",
                "headers": {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN', '')}"},
            }
        }
    )

    tools = await mcp_client.get_tools()
    tools = [t for t in tools if t.name in ("list_issues", "search_code", "search_issues", "search_pull_requests")]

    prompt_path = Path(__file__).parent / "triager.prompt.md"
    with prompt_path.open("r", encoding="utf-8") as f:
        prompt = f.read()
    agent = create_agent(model, prompt=prompt, tools=tools, response_format=IssueProposal)

    user_content = "Find an issue from Azure-samples azure-search-openai-demo that can be closed."
    async for step in agent.astream({"messages": [HumanMessage(content=user_content)]}, stream_mode="updates"):
        for step_name, step_data in step.items():
            last_message = step_data["messages"][-1]
            if isinstance(last_message, AIMessage) and last_message.tool_calls:
                tool_name = last_message.tool_calls[0]["name"]
                tool_args = last_message.tool_calls[0]["args"]
                logger.info(f"Calling tool '{tool_name}' with args:\n{tool_args}")
            elif isinstance(last_message, ToolMessage):
                logger.info(f"Got tool result:\n{last_message.content[0:200]}...")
            if step_data.get("structured_response"):
                print(step_data["structured_response"])


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    asyncio.run(main())
