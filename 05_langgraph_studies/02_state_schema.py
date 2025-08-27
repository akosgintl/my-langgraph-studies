# TypedDict example

from typing import Literal, TypedDict

class TypedDictState(TypedDict):
    name: str
    mood: Literal["happy","sad"]

import random
from langgraph.graph import StateGraph, START, END

def node_1(state):
    print("---Node 1---")
    return {"name": state['name'] + " is ... "}

def node_2(state):
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(state):
    print("---Node 3---")
    return {"mood": "sad"}

def decide_mood(state) -> Literal["node_2", "node_3"]:
        
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "node_2"
    
    # 50% of the time, we return Node 3
    return "node_3"

# Build graph
builder = StateGraph(TypedDictState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

output_typeddict = graph.invoke({"name":"Jack"})


# Dataclass example

from dataclasses import dataclass

@dataclass
class DataclassState:
    name: str
    mood: Literal["happy","sad"]


def node_1(state):
    print("---Node 1---")
    return {"name": state.name + " is ... "}

# Build graph
builder = StateGraph(DataclassState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

output_dataclass = graph.invoke(DataclassState(name="Jack",mood="sad"))


# Pydantic example

from pydantic import BaseModel, field_validator, ValidationError

class PydanticState(BaseModel):
    name: str
    mood: str # "happy" or "sad" 

    @field_validator('mood')
    @classmethod
    def validate_mood(cls, value):
        # Ensure the mood is either "happy" or "sad"
        if value not in ["happy", "sad"]:
            raise ValueError("Each mood must be either 'happy' or 'sad'")
        return value

# Build graph
builder = StateGraph(PydanticState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

output_pydantic = graph.invoke(PydanticState(name="Jack",mood="sad"))

# DIPLAY OUTPUTS

print("--------------------------------")
print("Pydantic validation:")
print("--------------------------------")
try:
    state = PydanticState(name="John Doe", mood="mad")
except ValidationError as e:
    print("Validation Error:", e)

print("--------------------------------")
print("Pydantic:")
print("--------------------------------")
print("---print---")
print(output_pydantic)

print("---pprint---")
from pprint import pprint
pprint(output_pydantic)

print("---pprint(ident=0, compact=True)---")
pprint(output_pydantic, indent=0, compact=True)

print("---json.dumps(indent=2)---")
import json
print(json.dumps(output_pydantic, indent=2))

print("--------------------------------")
print("TypedDict:")
print("--------------------------------")
print("---print---")
print(output_typeddict)

print("---pprint---")
from pprint import pprint
pprint(output_typeddict)

print("---pprint(ident=0, compact=True)---")
pprint(output_typeddict, indent=0, compact=True)

print("---json.dumps(indent=2)---")
import json
print(json.dumps(output_typeddict, indent=2))

print("--------------------------------")
print("Dataclass:")
print("--------------------------------")
print("---print---")
print(output_dataclass)

print("---pprint---")
from pprint import pprint
pprint(output_dataclass)

print("---pprint(ident=0, compact=True)---")
pprint(output_dataclass, indent=0, compact=True)

print("---json.dumps(indent=2)---")
import json
print(json.dumps(output_dataclass, indent=2))

print("--------------------------------")
