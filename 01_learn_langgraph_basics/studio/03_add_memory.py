#!/usr/bin/env python3
"""
3. Add memory to LangGraph chatbot
"""


from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition


class State(MessagesState):
    """State definition for the chatbot graph"""
    pass


def chatbot(state: State):
    """Chatbot node that processes user messages"""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


    
tool = TavilySearch(max_results=2)
tools = [tool]
tool_node = ToolNode(tools=[tool])

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
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()
