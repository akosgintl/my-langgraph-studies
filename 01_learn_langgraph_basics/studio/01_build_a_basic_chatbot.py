#!/usr/bin/env python3
"""
1. Build a basic chatbot
"""


from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langchain.chat_models import init_chat_model


class State(MessagesState):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    pass


def chatbot(state: State):
    """Chatbot node function that processes messages and returns LLM response"""
    return {"messages": [llm.invoke(state["messages"])]}


def stream_graph_updates(graph, user_input: str):
    """Stream graph updates and print assistant responses"""
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


llm = init_chat_model("openai:gpt-4.1")

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
