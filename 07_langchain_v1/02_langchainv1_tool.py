import logging
import os
import random

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from rich import print
from rich.logging import RichHandler

# Setup logging with rich
logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("weekend_planner")

load_dotenv(override=True)
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

@tool
def get_weather(city: str) -> dict:
    """Returns weather data for a given city, a dictionary with temperature and description."""
    logger.info(f"Getting weather for {city}")
    if random.random() < 0.05:
        return {
            "temperature": 72,
            "description": "Sunny",
        }
    else:
        return {
            "temperature": 60,
            "description": "Rainy",
        }


agent = create_agent(
    model=model,
    prompt="You are an informational agent. Answer questions cheerfully.",
    tools=[get_weather],
)


def main():
    response = agent.invoke({"messages": [{"role": "user", "content": "what's the weather in San Francisco today?"}]})
    latest_message = response["messages"][-1]
    print(latest_message.content)


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    main()
