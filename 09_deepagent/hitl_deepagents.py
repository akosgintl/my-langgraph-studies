import os
from typing import no_type_check

from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


load_dotenv()

@tool
def send_email(content: str, recepient:str):
    """Send an email to the recepient with the content"""
    print(f"Sending email to {recepient} with content: {content}")
    return "Email sent successfully"

# Without Human-in-the-loop
prompt = "You are a helpful email assistant. Email content and recipient are equally important in the message."
agent = create_deep_agent([send_email], prompt)

# Required for Human-in-the-loop
checkpointer = InMemorySaver()
agent.checkpointer = checkpointer

message = "Tell jim@example.com ill be late"

# No Human-in-the-loop
print("\n\n--------------------------------")
print("--- No Human-in-the-loop ---")

config = {"configurable": {"thread_id": "1-accept"}}
for s in agent.stream({"messages": [{"role": "user", "content": message}]}, config=config):
    print("--------------------------------")
    print(s)


# With Human-in-the-loop
print("\n\n--------------------------------")
print("--- With Human-in-the-loop ---")

hitl_config = {"send_email": True}

prompt = "You are a helpful email assistant. Email content and recipient are equally important in the message."
agent = create_deep_agent([send_email], prompt, interrupt_config=hitl_config)

# Required for Human-in-the-loop
checkpointer = InMemorySaver()
agent.checkpointer = checkpointer

message = "Tell jim@example.com ill be late"

# Accept
print("\n\n--------------------------------")
print("--- Accept ---")

config = {"configurable": {"thread_id": "1-accept"}}
for s in agent.stream({"messages": [{"role": "user", "content": message}]}, config=config):
    print("--------------------------------")
    print(s)

print("\n\n--------------------------------")
print("...Command Accept ...")

for s in agent.stream(Command(resume=[{"type": "accept"}]), config=config):
    print("--------------------------------")
    print(s)

# Edit
print("\n\n--------------------------------")
print("--- Edit ---")

config = {"configurable": {"thread_id": "2-edit"}}
for s in agent.stream({"messages": [{"role": "user", "content": message}]}, config=config):
    print("--------------------------------")
    print(s)

print("\n\n--------------------------------")
print("... Command Edit ...")

args = {"action": "send_email", "args": {"content": "sorry i will be late!", "recepient": "jim@gmail.com"}}
for s in agent.stream(Command(resume=[{"type": "edit", "args": args}]), config=config):
    print("--------------------------------")
    print(s)

# Response
print("\n\n--------------------------------")
print("--- Response ---")

config = {"configurable": {"thread_id": "3-response"}}
for s in agent.stream({"messages": [{"role": "user", "content": message}]}, config=config):
    print("--------------------------------")
    print(s)

print("\n\n--------------------------------")
print("... Command Response ...")

hitl_response = """ERROR: user interrupted with feedback:

Sign it from Harrison"""
for s in agent.stream(Command(resume=[{"type": "response", "args": hitl_response}]), config=config):
    print("--------------------------------")
    print(s)

print("\n\n--------------------------------")
print("... Command Accept ...")

for s in agent.stream(Command(resume=[{"type": "accept"}]), config=config):
    print("--------------------------------")
    print(s)
