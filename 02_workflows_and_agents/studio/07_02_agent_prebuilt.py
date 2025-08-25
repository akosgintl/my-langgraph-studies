from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from util import get_openai_api_key, save_workflow_png
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


# Define tools
@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", api_key=get_openai_api_key())

tools = [add, multiply, divide]

# Create the agent
agent = create_react_agent(llm, tools=tools)
