#!/usr/bin/env python3
"""
1. Build a basic chatbot
"""

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# from typing import Annotated, TypedDict
# from langchain_core.messages import BaseMessage
# from langgraph.graph.message import add_messages


# Using MessagesState
# class State(MessagesState):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
#     pass

# Equivalent if we use TypedDict
# class State(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# Using directly MessagesState
def chatbot(state: MessagesState):
    """Chatbot node function that processes messages and returns LLM response"""
    return {"messages": [llm.invoke(state["messages"])]}

# Using TypedDict
# def chatbot(state: State):
    # """Chatbot node function that processes messages and returns LLM response"""
    # return {"messages": [llm.invoke(state["messages"])]}

# Load the environment variables (OPENAI_API_KEY)
load_dotenv()

# Initialize the LLM
llm = init_chat_model("openai:gpt-4o-mini")

# Build the graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# Invoke the graph
output = graph.invoke({"messages": [HumanMessage(content="Hello, how are you?")]})

# Print the output
for message in output["messages"]:
    message.pretty_print()

print("--------------------------------")
print("--- MessagesState ---")
print(output)
