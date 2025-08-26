from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools.retriever import create_retriever_tool
from typing_extensions import Literal
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import END, START, StateGraph, MessagesState
from utils import save_workflow_png, format_retriever_results, get_anthropic_api_key, format_messages
from langchain_anthropic import ChatAnthropic


# Let's index a few of Lilian Weng's blog posts
urls = [
    "https://lilianweng.github.io/posts/2025-05-01-thinking/",
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]

# Load documents from each URL
docs = [WebBaseLoader(url).load() for url in urls]


# Flatten the list of documents
docs_list = [item for sublist in docs for item in sublist]

# Initialize text splitter 
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=2000, 
    chunk_overlap=50
)

# Split documents into chunks
doc_splits = text_splitter.split_documents(docs_list)

# Initialize embeddings model
embeddings = init_embeddings("openai:text-embedding-3-small")

# Create in memory vector store from documents
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, 
    embedding=embeddings
)

# Create retriever from vector store
retriever = vectorstore.as_retriever()

# Results are a list of Document objects
r = retriever.invoke("types of reward hacking")

# Create retriever tool
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng blog posts.",
)

# Test the retriever tool
# result = retriever_tool.invoke({"query": "types of reward hacking"})
# format_retriever_results(result[10:1000])


# Initialize language model
llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0, anthropic_api_key=get_anthropic_api_key())

# Bind tools
tools = [retriever_tool]
tools_by_name = {tool.name: tool for tool in tools}

# Bind tools to LLM for agent functionality
llm_with_tools = llm.bind_tools(tools)

# Define the RAG agent system prompt
rag_prompt = """You are a helpful assistant tasked with retrieving information from a series of technical blog posts by Lilian Weng. 
Clarify the scope of research with the user before using your retrieval tool to gather context. Reflect on any context you fetch, and
proceed until you have sufficient context to answer the user's research request."""

def llm_call(state: MessagesState) -> dict:
    """LLM decides whether to call a tool or not.
    
    Args:
        state: Current conversation state
        
    Returns:
        Dictionary with new messages
    """
    return {
        "messages": [
            llm_with_tools.invoke(
                [SystemMessage(content=rag_prompt)] + state["messages"]
            )
        ]
    }
    
def tool_node(state: MessagesState) -> dict:
    """Performs the tool call.
    
    Args:
        state: Current conversation state with tool calls
        
    Returns:
        Dictionary with tool results
    """
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: MessagesState) -> Literal["tool_node", "__end__"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call.
    
    Args:
        state: Current conversation state
        
    Returns:
        Next node to execute
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"
    # Otherwise, we stop (reply to the user)
    return END

# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
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

# Compile the agent
agent = agent_builder.compile()

# Save the agent
save_workflow_png(agent, "01_rag.png")


# Execute the RAG agent
query = "What are the types of reward hacking discussed in the blogs?"
result = agent.invoke({"messages": [{"role": "user", "content": query}]})

# Format and display results
format_messages(result['messages'])