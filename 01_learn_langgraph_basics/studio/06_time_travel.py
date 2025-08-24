"""
Time Travel Chatbot using LangGraph
"""

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from langgraph.graph import StateGraph, START
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition


class State(MessagesState):
    pass


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


tool = TavilySearch(max_results=2)
tools = [tool]

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=[tool]))
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

# Step 1:
#       {
#            "messages": [
#                {
#                    "role": "user",
#                    "content": (
#                        "I'm learning LangGraph.js. "
#                        "Could you do some research on it for me?"
#                    ),
#                },
#            ],
#        }

# Step 2:
# 
#        {
#            "messages": [
#                {
#                    "role": "user",
#                    "content": (
#                        "Ya that's helpful. Maybe I'll "
#                        "build an network type multi-agent with it!"
#                    ),
#                },
#            ],
#        },







