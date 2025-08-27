from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State
class State(TypedDict):
    name: str
   
# Node
def node_1(state: State):
    print("---Node1---")
    print(f"{state}")

    return {"name": "node_1"}

# Build graph
builder = StateGraph(State)
# Add nodes to the graph
builder.add_node("node_1", node_1)
# Add edges to the graph
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)
# Compile the graph
graph = builder.compile()


# Invoke the graph

input = {"name": "start"}

result = graph.invoke(input)

print("---result---")
print(f"{result}")
