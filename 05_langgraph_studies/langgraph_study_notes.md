# My Progressive Study Notes

## 1. Basic Graph - Graph Basics

Based on: [Graph API Concepts](https://docs.langchain.com/oss/python/graph-api)

At its core, LangGraph models agent workflows as graphs. You define the behavior of your agents using three key components:

1. `State`: A shared data structure that represents the current snapshot of your application.

2. `Nodes`: Functions that encode the logic of your agents. They receive the current state as input, perform some computation or side-effect, and return an updated state.

3. `Edges`: Functions that determine which `Node` to execute next based on the current state.

By composing `Nodes` and `Edges`, you can create complex, looping workflows that evolve the `State` over time. To emphasize: `Nodes` and `Edges` are nothing more than functions - they can contain an LLM or just good ol' code.

In short: _nodes do the work, edges tell what to do next_.

### [StateGraph](https://langchain-ai.github.io/langgraph/reference/graphs/)

The `StateGraph` class is the main graph class to use. This is parameterized by a user defined `State` object.

### [State](https://docs.langchain.com/oss/python/graph-api#state)

The first thing you do when you define a graph is define the `State` of the graph. The `State` consists of the **Schema of the Graph**. The schema of the `State` will be the input schema to all `Nodes` and `Edges` in the graph. All `Nodes` will emit updates to the `State`.

## [Nodes](https://docs.langchain.com/oss/python/graph-api#nodes)

In LangGraph, nodes are Python functions that accept the `state`: The [state](#state) of the graph

You add these nodes to a graph using the [add\_node](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph.add_node) method.

## [Edges](https://docs.langchain.com/oss/python/graph-api#edges)

Edges define how the logic is routed and how the graph decides to stop. This is a big part of how your agents work and how different nodes communicate with each other.

## Special Nodes to build the Graph

### `START` Node

The `START` Node is a special node that represents the node that sends user input to the graph. The main purpose for referencing this node is to determine which nodes should be called first.

### `END` Node

The `END` Node is a special node that represents a terminal node. This node is referenced when you want to denote which edges have no actions after they are done.

## Compiling your graph

The last step of building your graph is compiling it.

Compiling is a pretty simple step. It provides a few basic checks on the structure of your graph (no orphaned nodes, etc). You compile your graph by just calling the `.compile` method

## Example

Setup:

```bash

pip install -U langgraph

```

```python

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State
class State(TypedDict):
    name: str
   
# Node
def node_1(state: State):
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

```

## Invoke the Graph

To invoke the Graph simply call the `.invoke` method with the initial user message:

```python

from langchain.schema import HumanMessage

# Invoke the graph
result = graph.invoke({"name": "start"})
print(result)

```


## 2. State

The first thing you do when you define a graph is define the `State` of the graph. The `State` consists of the [schema of the graph](#schema) as well as [`reducer` functions](#reducers) which specify how to apply updates to the state. The schema of the `State` will be the input schema to all `Nodes` and `Edges` in the graph, and can be either a `TypedDict` or a `Pydantic` model. All `Nodes` will emit updates to the `State` which are then applied using the specified `reducer` function.

### Schema

The main documented way to specify the schema of a graph is by using a [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict). If you want to provide default values in your state, use a [`dataclass`](https://docs.python.org/3/library/dataclasses.html). We also support using a Pydantic [BaseModel](https://docs.pydantic.dev/latest/api/base_model) as your graph state if you want recursive data validation (though note that pydantic is less performant than a `TypedDict` or `dataclass`).

By default, the graph will have the same input and output schemas. If you want to change this, you can also specify explicit input and output schemas directly. This is useful when you have a lot of keys, and some are explicitly for input and others for output. See the [guide here](https://langchain-ai.github.io/langgraph/how-tos/graph-api/#use-pydantic-models-for-graph-state) for how to use.

#### TypedDict example

[Example from](https://github.com/langchain-ai/langchain-academy/blob/main/module-2/state-schema.ipynb):

```python

from typing import Literal

class TypedDictState(TypedDict):
    name: str
    mood: Literal["happy","sad"]

```

#### Dataclasses example

[Example from](https://github.com/langchain-ai/langchain-academy/blob/main/module-2/state-schema.ipynb):

```python

from dataclasses import dataclass

@dataclass
class DataclassState:
    name: str
    mood: Literal["happy","sad"]

```

To access the keys of a `dataclass`, we just need to modify the subscripting used in `node_1`: 

* We use `state.name` for the `dataclass` state rather than `state["name"]` for the `TypedDict` above

#### Pydantic example with Validator

[Example from](https://github.com/langchain-ai/langchain-academy/blob/main/module-2/state-schema.ipynb):

```python
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

try:
    state = PydanticState(name="John Doe", mood="mad")
except ValidationError as e:
    print("Validation Error:", e)
```

`mood="mad"` will result ValidationError.

#### Print schemas

Print a `TypedDict` / `Dataclass` / `Pydantic` State you can use:

```python

print(output)

from pprint import pprint
pprint(output)

pprint(output, indent=0, compact=True)

import json
print(json.dumps(output, indent=2))
```

#### Multiple schemas

Typically, all graph nodes communicate with a single schema. This means that they will read and write to the same state channels. 

But, there are cases where we want more control over this:

- Internal nodes can pass information that is **not required** in the graph's input / output.
- We may also want to use different input / output schemas for the graph. The output might, for example, only contain a single **relevant** output key.

It is possible to have nodes write to `private state` channels inside the graph for internal node communication. We can simply define a private schema, `PrivateState`.

It is also possible to define explicit input and output schemas for a graph. In these cases, we define an "internal" schema that contains _all_ keys relevant to graph operations. But, we also define `input` and `output` schemas that are sub-sets of the "internal" schema to constrain the input and output of the graph. See [this guide](https://langchain-ai.github.io/langgraph/how-tos/graph-api/#define-input-and-output-schemas) for more detail.

```python
class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    graph_output: str

class OverallState(TypedDict):
    foo: str
    user_input: str     # Shared with InputState
    graph_output: str   # Shared with OutputState          

class PrivateState(TypedDict):
    bar: str

def node_1(state: InputState) -> OverallState:
    # Write to OverallState
    return {"foo": state["user_input"] + " name"}

def node_2(state: OverallState) -> PrivateState:
    # Read from OverallState, write to PrivateState
    return {"bar": state["foo"] + " is"}

def node_3(state: PrivateState) -> OutputState:
    # Read from PrivateState, write to OutputState
    return {"graph_output": state["bar"] + " Jack"}

builder = StateGraph(OverallState,input_schema=InputState,output_schema=OutputState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()
graph.invoke({"user_input":"My"})
# {'graph_output': 'My name is Jack'}
```

There are two subtle and important points to note here:

1. We pass `state: InputState` as the input schema to `node_1`. But, we write out to `foo`, a channel in `OverallState`. How can we write out to a state channel that is not included in the input schema? This is because a node _can write to any state channel in the graph state._ The graph state is the union of the state channels defined at initialization, which includes `OverallState` and the filters `InputState` and `OutputState`.

2. We initialize the graph with `StateGraph(OverallState,input_schema=InputState,output_schema=OutputState)`. So, how can we write to `PrivateState` in `node_2`? How does the graph gain access to this schema if it was not passed in the `StateGraph` initialization? We can do this because _nodes can also declare additional state channels_ as long as the state schema definition exists. In this case, the `PrivateState` schema is defined, so we can add `bar` as a new state channel in the graph and write to it.

### Reducers

Reducers are key to understanding how updates from nodes are applied to the `State`. Each key in the `State` has its own independent reducer function. If no reducer function is explicitly specified then it is assumed that all updates to that key should override it. There are a few different types of reducers, starting with the default type of reducer:

#### Default Reducer

These two examples show how to use the default reducer:

**Example A:**

```python
from typing_extensions import TypedDict

class State(TypedDict):
    foo: int
    bar: list[str]
```

In this example, no reducer functions are specified for any key. Let's assume the input to the graph is:

`{"foo": 1, "bar": ["hi"]}`. Let's then assume the first `Node` returns `{"foo": 2}`. This is treated as an update to the state. Notice that the `Node` does not need to return the whole `State` schema - just an update. After applying this update, the `State` would then be `{"foo": 2, "bar": ["hi"]}`. If the second node returns `{"bar": ["bye"]}` then the `State` would then be `{"foo": 2, "bar": ["bye"]}`


**Example B:**

```python
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    foo: int
    bar: Annotated[list[str], add]
```

For `TypedDict` state schemas, we can define reducers by annotating the corresponding field of the state with a reducer function.

In this example, we've used the `Annotated` type to specify a reducer function (`operator.add`) for the second key (`bar`). Note that the first key remains unchanged. Let's assume the input to the graph is `{"foo": 1, "bar": ["hi"]}`. Let's then assume the first `Node` returns `{"foo": 2}`. This is treated as an update to the state. Notice that the `Node` does not need to return the whole `State` schema - just an update. After applying this update, the `State` would then be `{"foo": 2, "bar": ["hi"]}`. If the second node returns `{"bar": ["bye"]}` then the `State` would then be `{"foo": 2, "bar": ["hi", "bye"]}`. Notice here that the `bar` key is updated by adding the two lists together.


### Working with Messages in Graph State

#### Why use messages?

Most modern LLM providers have a chat model interface that accepts a list of messages as input. LangChain's [`ChatModel`](https://python.langchain.com/docs/concepts/chat_models) in particular accepts a list of `Message` objects as inputs. These messages come in a variety of forms such as `HumanMessage` (user input) or `AIMessage` (LLM response). To read more about what message objects are, please refer to [this](https://python.langchain.com/docs/concepts/messages) conceptual guide.

#### Using Messages in your Graph

In many cases, it is helpful to store prior conversation history as a list of messages in your graph state. To do so, we can add a key (channel) to the graph state that stores a list of `Message` objects and annotate it with a reducer function (see `messages` key in the example below). The reducer function is vital to telling the graph how to update the list of `Message` objects in the state with each state update (for example, when a node sends an update). If you don't specify a reducer, every state update will overwrite the list of messages with the most recently provided value. If you wanted to simply append messages to the existing list, you could use `operator.add` as a reducer.

However, you might also want to manually update messages in your graph state (e.g. human-in-the-loop). If you were to use `operator.add`, the manual state updates you send to the graph would be appended to the existing list of messages, instead of updating existing messages. To avoid that, you need a reducer that can keep track of message IDs and overwrite existing messages, if updated. To achieve this, you can use the prebuilt `add_messages` function. For brand new messages, it will simply append to existing list, but it will also handle the updates for existing messages correctly.

In practice, there are additional considerations for updating lists of messages:
- We may wish to update an existing message in the state (see above)
- We may want to accept short-hands for message formats, such as [OpenAI format](https://python.langchain.com/docs/concepts/messages/#openai-format).
The built-in reducer add_messages handles these considerations.

#### Serialization

In addition to keeping track of message IDs, the `add_messages` function will also try to deserialize messages into LangChain `Message` objects whenever a state update is received on the `messages` channel. See more information on LangChain serialization/deserialization [here](https://python.langchain.com/docs/how_to/serialization/). This allows sending graph inputs / state updates in the following format:

```python
# this is supported
{"messages": [HumanMessage(content="message")]}

# and this is also supported
{"messages": [{"type": "human", "content": "message"}]}
```

Since the state updates are always deserialized into LangChain `Messages` when using `add_messages`, you should use dot notation to access message attributes, like `state["messages"][-1].content`. Below is an example of a graph that uses `add_messages` as its reducer function.

```python
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

#### MessagesState

Since having a list of messages in your state is so common, there exists a prebuilt state called `MessagesState` which makes it easy to use messages. `MessagesState` is defined with a single `messages` key which is a list of `AnyMessage` objects and uses the `add_messages` reducer. Typically, there is more state to track than just messages, so we see people subclass this state and add more fields, like:

```python
from langgraph.graph import MessagesState

class State(MessagesState):
    documents: list[str]
```

#### Complete example with LLM

```python

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Using MessagesState
def chatbot(state: MessagesState):
    """Chatbot node function that processes messages and returns LLM response"""
    return {"messages": [llm.invoke(state["messages"])]}

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

```

Print the output

```python

# Print the output
for message in output["messages"]:
    message.pretty_print()

```

## Edges

Edges define how the logic is routed and how the graph decides to stop. This is a big part of how your agents work and how different nodes communicate with each other. There are a few key types of edges:

- Normal Edges: Go directly from one node to the next.
- Conditional Edges: Call a function to determine which node(s) to go to next.
- Entry Point: Which node to call first when user input arrives.
- Conditional Entry Point: Call a function to determine which node(s) to call first when user input arrives.
- (Exit Point: Where the graph flow terminates)

A node can have MULTIPLE outgoing edges. If a node has multiple out-going edges, **all** of those destination nodes will be executed in parallel as a part of the next superstep.

### Normal Edges

If you **always** want to go from node A to node B, you can use the @[add_edge][add_edge] method directly.

```python
graph.add_edge("node_a", "node_b")
```

### Conditional Edges

If you want to **optionally** route to 1 or more edges (or optionally terminate), you can use the @[add_conditional_edges][add_conditional_edges] method. This method accepts the name of a node and a "routing function" to call after that node is executed:

```python
graph.add_conditional_edges("node_a", routing_function)
```

Similar to nodes, the `routing_function` accepts the current `state` of the graph and returns a value.

By default, the return value `routing_function` is used as the **name of the node** (or list of nodes) to send the state to next. All those nodes will be run in parallel as a part of the next superstep.

You can optionally provide a dictionary that maps the `routing_function`'s output to the name of the next node.

```python
graph.add_conditional_edges("node_a", routing_function, {True: "node_b", False: "node_c"})
```

<Tip>

    Use [`Command`](#command) instead of conditional edges if you want to combine state updates and routing in a single function.

</Tip>

### Entry Point

The entry point is the first node(s) that are run when the graph starts. You can use the @[`add_edge`][add_edge] method from the virtual @[`START`][START] node to the first node to execute to specify where to enter the graph.

```python
from langgraph.graph import START

graph.add_edge(START, "node_a")
```

The `START` node is equivalent to `"__start__"`

### Conditional Entry Point

A conditional entry point lets you start at different nodes depending on custom logic. You can use @[`add_conditional_edges`][add_conditional_edges] from the virtual @[`START`][START] node to accomplish this.

```python
from langgraph.graph import START

graph.add_conditional_edges(START, routing_function)
```

You can optionally provide a dictionary that maps the `routing_function`'s output to the name of the next node.

```python
graph.add_conditional_edges(START, routing_function, {True: "node_b", False: "node_c"})
```

### `END` Node

The `END` Node is a special node that represents a terminal node. This node is referenced when you want to denote which edges have no actions after they are done.

The `END` node is equivalent to `"__end__"`

### Example

The [example](06_conditional_edges.py) is based on [this](https://github.com/langchain-ai/langchain-academy/blob/main/module-1/studio/simple.py) code.
 
## Nodes

llm
tools

filter and trim messages
context management - summary,...

## Multiple state

sub-agents
reducers
parallelization
```
create_react_agent

structured output

init
API keys

## pre-builts

supervisor
swarm
mcp

langmem

(agentevals)

## 4. LLMs and Prompts

SystemPrompt
UserPrompt
ChatTemplates


## 5. LLMs and Messages

MessagesState
HumanMessage
AIMessage
ToolMessage

format_messages

## Graph visualizing

## Graph checkpointing and config

## Graph config

## invoke vs. stream

## sync vs. async

## Send vs. Command

## HIL

## Memory

short-term (checkpointing)
long-term

## Sub-graphs
## Reflection

## Agentic rag

adaptive
crag
self-rag

## Multi-agent

handoffs
network
supervisor
hierachical

map-reduce

## Others

docs/docs/tutorials