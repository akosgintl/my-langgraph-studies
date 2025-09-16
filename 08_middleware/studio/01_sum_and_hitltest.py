from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from dotenv import load_dotenv

load_dotenv(override=True)

model = ChatOpenAI(model="gpt-4o-mini")
prompt = "You are a helpful assistant that can perform addition, subtraction, multiplication, and division. Use the tools sequentially to perform the operations."

def addition(a: int, b: int) -> int:
    """Add a and b."""
    return a + b

def subtraction(a: int, b: int) -> int:
    """Subtract a and b."""
    return a - b

def multiplication(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b

def division(a: int, b: int) -> int:
    """Divide a and b."""
    return a / b

tools = [addition, subtraction, multiplication, division]

memory = InMemorySaver()
config = {"configurable": {"thread_id": "1"}}

agent = create_agent(
    model=model,
    prompt=prompt,
    tools=tools,
    middleware=[
        SummarizationMiddleware(
            model=model,
            max_tokens_before_summary=100,  # Trigger summarization at 4000 tokens
            messages_to_keep=2,  # Keep last 20 messages after summary
            # summary_prompt="Custom prompt for summarization...",  # Optional
        ),
        HumanInTheLoopMiddleware(
            tool_configs={
                "addition": {
                    "require_approval": True,
                    "description": "⚠️ Addition operation requires approval",
                },
                "subtraction": {
                    "require_approval": True,
                    "description": "🚨 Subtraction operation requires approval",
                },
                "multiplication": {
                    "require_approval": True,  # Safe operation, no approval needed
                    "description": "🚨 Multiplication operation requires approval",
                },
                "division": {
                    "require_approval": True,  # Safe operation, no approval needed
                    "description": "🚨 Division operation requires approval",
                },
            },
            message_prefix="Tool execution pending approval",
        ),
    ],
    # checkpointer=memory,
)
