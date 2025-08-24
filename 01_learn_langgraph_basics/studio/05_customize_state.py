"""
Custom State Chatbot using LangGraph
"""


from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langchain_tavily import TavilySearch

from langgraph.types import Command, interrupt
from langgraph.graph import StateGraph, START
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition


class State(MessagesState):
    name: str
    birthday: str


@tool
def human_assistance(
    name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
) -> str:
    """Request assistance from a human."""
    human_response = interrupt(
        {
            "question": "Is this correct?",
            "name": name,
            "birthday": birthday,
        }
    )
    
    # If the information is correct, update the state as-is
    if human_response.get("correct", "").lower().startswith("y"):
        verified_name = name
        verified_birthday = birthday
        response = "Correct"
    # Otherwise, receive information from the human reviewer
    else:
        verified_name = human_response.get("name", name)
        verified_birthday = human_response.get("birthday", birthday)
        response = f"Made a correction: {human_response}"

    # Update the state with verified information
    state_update = {
        "name": verified_name,
        "birthday": verified_birthday,
        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
    }
    
    # Return a Command object to update the state
    return Command(update=state_update)

    
def chatbot(state: State):
    """Chatbot node that processes messages and may call tools."""
    message = llm_with_tools.invoke(state["messages"])
    # Disable parallel tool calling to avoid repeating tool invocations during human review
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

search_tool = TavilySearch(max_results=2)
tools = [search_tool, human_assistance]
tool_node = ToolNode(tools=tools)

llm = init_chat_model("openai:gpt-4o-mini")
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
# Can you look up when LangGraph was released? When you have the answer, use the human_assistance tool for review.

# Step 2:
# Interrupt
# 2021-12-01
# LangGraph
# Is this correct?

# Step 3:
# {
#   "correct": "no",
#   "name" : "LangGraph",
#   "birthday" : "2024-02-20"
# }


