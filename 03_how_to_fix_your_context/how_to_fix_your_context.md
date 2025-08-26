# How to Fix Your Context

https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html

## Problem

Briefly recap some of the ways long contexts can fail:

- **Context Poisoning**: When a hallucination or other error makes it into the context, where it is repeatedly referenced.
- **Context Distraction**: When a context grows so long that the model over-focuses on the context, neglecting what it learned during training.
- **Context Confusion**: When superfluous information in the context is used by the model to generate a low-quality response.
- **Context Clash**: When you accrue new information and tools in your context that conflicts with other information in the prompt.

# Proposed solutions

Context Management Tactics:

- **RAG**: Selectively adding relevant information to help the LLM generate a better response
- **Tool Loadout**: Selecting only relevant tool definitions to add to your context
- **Context Quarantine**: Isolating contexts in their own dedicated threads
- **Context Pruning**: Removing irrelevant or otherwise unneeded information from the context
- **Context Summarization**: Boiling down an accrued context into a condensed summary
- **Context Offloading**: Storing information outside the LLM's context, usually via a tool that stores and manages the data

# Implementations in LangGraph

https://github.com/langchain-ai/how_to_fix_your_context/blob/main/README.md

## 1. RAG (Retrieval-Augmented Generation)

**Notebook**: [01-rag.py](01-rag.py)

*Retrieval-Augmented Generation (RAG) is the act of selectively adding relevant information to help the LLM generate a better response.*

**Implementation**: Creates a RAG agent using LangGraph with a retrieval tool built from Lilian Weng's blog posts. The agent uses Claude Sonnet to intelligently search for relevant context before answering questions.

**Key Components**:
- Document loading and chunking with RecursiveCharacterTextSplitter
- Vector store creation using OpenAI embeddings
- LangGraph StateGraph with conditional edges for tool calling
- System prompt that guides the agent to clarify research scope before retrieval

**Performance**: Used 25k tokens for a complex query about reward hacking types, driven by token-heavy tool calls.

### 2. Tool Loadout

**Notebook**: [02_tool_loadout.py](02_tool_loadout.py)

*Tool Loadout is the act of selecting only relevant tool definitions to add to your context.*

**Implementation**: Demonstrates semantic tool selection by indexing all Python math library functions in a vector store and dynamically selecting only relevant tools based on user queries.

**Key Components**:
- Tool registry with UUID mapping for all math functions
- Vector store indexing of tool descriptions using embeddings
- Dynamic tool binding based on semantic similarity search (limit 5 tools)
- Extended state class to track selected tools per conversation

**Benefits**: Avoids context confusion from overlapping tool descriptions and improves tool selection accuracy compared to loading all available tools.

### 3. Context Quarantine

**Notebook**: [03_context_quarantine.py](03_context_quarantine.py)

*Context Quarantine is the act of isolating contexts in their own dedicated threads, each used separately by one or more LLMs.*

**Implementation**: Creates a supervisor multi-agent system using LangGraph Supervisor architecture with specialized agents that have isolated context windows.

**Key Components**:
- Supervisor agent that routes tasks to appropriate specialists
- Math expert agent with addition/multiplication tools and focused mathematical prompt
- Research expert agent with web search capabilities and research-focused prompt
- Clear delegation rules based on task type (research vs. calculations)

**Benefits**: Each agent operates in its own context window, preventing context clash and distraction. The supervisor coordinates between agents using tool-based handoffs for complex tasks requiring multiple skills.

### 4. Context Pruning

**Notebook**: [04_context_pruning.py](04_context_pruning.py)

*Context Pruning is the act of removing irrelevant or otherwise unneeded information from the context.*

**Implementation**: Extends the RAG agent with an intelligent pruning step that removes irrelevant content from retrieved documents before passing them to the main LLM.

**Key Components**:
- Tool pruning prompt that instructs a smaller LLM to extract only relevant information
- GPT-4o-mini as the pruning model to reduce costs
- Extended state class with summary field for context compression
- Pruning based on the original user request to maintain relevance

**Performance Improvement**: Reduced token usage from 25k to 11k tokens for the same query compared to basic RAG, demonstrating significant context compression while maintaining answer quality.

### 5. Context Summarization

**Notebook**: [05_context_summarization.py](05_context_summarization.py)

*Context Summarization is the act of boiling down an accrued context into a condensed summary.*

**Implementation**: Builds on the RAG agent by adding a summarization step that condenses tool call results to reduce context size while preserving essential information.

**Key Components**:
- Tool summarization prompt that creates comprehensive yet concise versions of documents
- GPT-4o-mini as the summarization model for cost efficiency
- Guidelines to preserve all key information while eliminating verbosity (50-70% reduction target)
- Extended state class with summary field for tracking condensed content

**Approach**: Unlike pruning which removes irrelevant content, summarization condenses all information into a more compact format, making it suitable when all retrieved content is relevant but verbose.

### 6. Context Offloading

**Notebook**: [06_context_offloading.py](06_context_offloading.py)

*Context Offloading is the act of storing information outside the LLM's context, usually via a tool that stores and manages the data.*

**Implementation**: Demonstrates two approaches to context offloading - temporary scratchpad storage during a session and persistent cross-thread memory using LangGraph's store interface.

**Key Components**:
- Extended state class with scratchpad field for temporary storage
- WriteToScratchpad and ReadFromScratchpad tools for note-taking
- InMemoryStore for persistent cross-thread memory
- Research workflow that maintains organized notes and builds upon previous research

**Two Storage Patterns**:
1. **Session Scratchpad**: Temporary storage within a single conversation thread
2. **Persistent Memory**: Cross-thread storage using namespaced key-value pairs that persist across different conversation sessions

**Benefits**: Enables agents to maintain research plans, accumulate findings, and access previous work across multiple interactions, similar to how Anthropic's multi-agent researcher and products like ChatGPT implement memory.
