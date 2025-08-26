import math  
import types
import uuid

from langchain.embeddings import init_embeddings

from langgraph.store.memory import InMemoryStore
from langgraph_bigtool.utils import convert_positional_only_function_to_tool

from utils import save_workflow_png, format_messages
from langchain_anthropic import ChatAnthropic
from utils import get_anthropic_api_key, get_openai_api_key
from typing import Dict, Any
from typing_extensions import Literal
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langgraph.store.base import BaseStore
from langgraph.graph import END, START, StateGraph, MessagesState


# Initialize the primary language model for the agent
llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0, anthropic_api_key=get_anthropic_api_key())

# Extract and convert all mathematical functions from Python's math module
all_tools = []
for function_name in dir(math):
    function = getattr(math, function_name)
    
    # Only process built-in mathematical functions
    if not isinstance(function, types.BuiltinFunctionType):
        continue
        
    # Convert math functions to LangChain tools (handles positional-only parameters)
    if tool := convert_positional_only_function_to_tool(function):
        all_tools.append(tool)

# Create a tool registry mapping unique IDs to tool instances
# This allows for efficient tool lookup and management
tool_registry = {
    str(uuid.uuid4()): tool
    for tool in all_tools
}

# Set up vector store for semantic tool search
# Uses embeddings to enable similarity-based tool selection
embeddings = init_embeddings("openai:text-embedding-3-small", openai_api_key=get_openai_api_key())

store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1536,  # OpenAI embedding dimensions
        "fields": ["description"],  # Index tool descriptions for search
    }
)

# Index all tools in the store for semantic similarity search
for tool_id, tool in tool_registry.items():
    store.put(
        ("tools",),  # Namespace for tool storage
        tool_id,
        {
            "description": f"{tool.name}: {tool.description}",
        },
    )


# Extended state class to store dynamically selected tools
class ToolLoadoutState(MessagesState):
    """State that extends MessagesState to include dynamically selected tools.
    
    This allows the agent to maintain context about which tools are currently
    available and bound to the conversation.
    """
    tools_by_name: Dict[str, Any] = {}

# System prompt defining the agent's role and capabilities
system_prompt = """You are a helpful assistant with access to mathematical functions from Python's math library. 
You can search for and use relevant mathematical tools to solve problems. 
When you need to perform mathematical calculations, first determine what type of mathematical operation you need, 
then use the appropriate tools from the math library."""

def llm_call(state: ToolLoadoutState, store: BaseStore) -> dict:
    """Main LLM call that dynamically selects and binds relevant tools.
    
    This function implements the core tool loadout pattern:
    1. Extract query context from user message
    2. Search for semantically relevant tools  
    3. Bind only relevant tools to the LLM
    4. Generate response with focused tool set
    
    Args:
        state: Current conversation state containing messages and tools
        store: Vector store containing indexed tool descriptions
        
    Returns:
        Dictionary with new messages and updated tool registry
    """
    # Extract user query for semantic tool search
    messages = state["messages"]
    if messages and isinstance(messages[-1], HumanMessage):
        query = messages[-1].content
    else:
        query = "mathematical calculation"  # Default fallback
    
    # Perform semantic similarity search to find relevant tools
    search_results = store.search(("tools",), query=query, limit=5)
    
    # Build focused tool set from search results
    relevant_tools = []
    tools_by_name = {}
    
    for result in search_results:
        tool_id = result.key
        if tool_id in tool_registry:
            tool = tool_registry[tool_id]
            relevant_tools.append(tool)
            tools_by_name[tool.name] = tool
    
    # Bind only relevant tools to avoid context overload
    llm_with_tools = llm.bind_tools(relevant_tools) if relevant_tools else llm
    
    # Generate response with focused context
    response = llm_with_tools.invoke(
        [SystemMessage(content=system_prompt)] + state["messages"]
    )
    
    return {
        "messages": [response],
        "tools_by_name": tools_by_name
    }

def tool_node(state: ToolLoadoutState) -> dict:
    """Execute tool calls using the dynamically selected tool set.
    
    Args:
        state: Current conversation state with tool calls
        
    Returns:
        Dictionary with tool execution results
    """
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        # Retrieve tool from the focused set stored in state
        tool = state["tools_by_name"][tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: ToolLoadoutState) -> Literal["tool_node", "__end__"]:
    """Determine workflow continuation based on tool calls.
    
    Args:
        state: Current conversation state
        
    Returns:
        Next node name or END
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # Continue to tool execution if LLM made tool calls
    if last_message.tool_calls:
        return "tool_node"
    
    # Otherwise end the conversation
    return END

# Build the tool loadout workflow
agent_builder = StateGraph(ToolLoadoutState)

# Add workflow nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Define workflow edges
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "tool_node": "tool_node",
        END: END,
    },
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent with tool store for semantic search
agent = agent_builder.compile(store=store)

# Display the workflow graph
save_workflow_png(agent, "02_tool_loadout.png")




query = "Use available tools to calculate arc cosine of 0.5."
result = agent.invoke({"messages": [HumanMessage(content=query)]})
format_messages(result['messages'])