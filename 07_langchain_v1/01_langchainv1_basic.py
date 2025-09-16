import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from rich import print

load_dotenv(override=True)
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

agent = create_agent(model=model, prompt="You're an informational agent. Answer questions cheerfully.", tools=[])

def main():
    response = agent.invoke({"messages": [{"role": "user", "content": "Whats weather today in San Francisco?"}]})
    latest_message = response["messages"][-1]
    print(latest_message.content)


if __name__ == "__main__":
    main()
