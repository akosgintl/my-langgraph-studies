from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from util import get_openai_api_key
from pprint import pprint


# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", api_key=get_openai_api_key())


# STRUCTURED OUTPUT

# Define a schema for structured output
class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query that is optimized web search.")
    justification: str = Field(
        None, description="Why this query is relevant to the user's request."
    )


# Augment the LLM with schema for structured output
structured_llm = llm.with_structured_output(SearchQuery)


# Invoke the augmented LLM
output = structured_llm.invoke("How does Calcium CT score relate to high cholesterol?")


# Print the output
print("--------------------------------")
print("# Structured output:", llm.model_name)
pprint(output, indent=0, compact=True)


# TOOL CALLING

# Define a tool
def multiply(a: int, b: int) -> int:
    return a * b


# Augment the LLM with tools
llm_with_tools = llm.bind_tools([multiply])


# Invoke the LLM with input that triggers the tool call
output = llm_with_tools.invoke("What is 2 times 3?")


# Print the tool call
print("--------------------------------")
print("# Tool call:", llm_with_tools.model_name)
output.pretty_print()
