#!/usr/bin/env python3
"""
4. Add human-in-the-loop controls
"""

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt


class State(MessagesState):
    pass


# Add the human_assistance tool
@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
        
    # This will pause execution and wait for human input
    human_response = interrupt({"query": query})
    # The response from interrupt is a Command object, not a dict
    return human_response["data"]


def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}


search_tool = TavilySearch(max_results=2)
tools = [search_tool, human_assistance]
tool_node = ToolNode(tools=tools)

llm = init_chat_model("openai:gpt-4.1")
llm_with_tools = llm.bind_tools(tools)

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
    
graph = graph_builder.compile()



# Step 1:
# I need some expert guidance for building an AI agent. Could you request assistance for me?

# Step 2:
# The user is seeking expert guidance for building an AI agent. Please provide direct support, tailored resources, or connect them with a specialist to assist in designing and developing an effective AI agent.

# Step 3:
# {
# "query": "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent. It's much more reliable and extensible than simple autonomous agents."
# }

