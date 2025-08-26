# My LangGraph Studies

## Setup

```bash
# Create virtual environment
python -m venv .venv --upgrade-deps

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Before running the chatbot, you need to set up your OpenAI, Tavily and (optinally) LangSmith API key:

1. **Create a `.env` file** in the project root directory
2. **Add your API keys** to the file:
   ```
   OPENAI_API_KEY=your_actual_api_key_here

   TAVILY_API_KEY=your_actual_api_key_here

   (optional)
   LANGCHAIN_API_KEY=your_actual_api_key_here
   ```
3. **See `env_example.txt`** for a complete example

**Important**: Never commit your `.env` file to version control. Add it to your `.gitignore` file.

### LangSmith Integration

Sign up for LangSmith to quickly spot issues and improve the performance of your LangGraph projects. LangSmith lets you use trace data to debug, test, and monitor your LLM apps built with LangGraph. For more information on how to get started, see [LangSmith docs](https://docs.smith.langchain.com).


## Step 1 - [Learn LangGraph Basics](https://docs.langchain.com/langgraph-platform/langgraph-basics/why-langgraph#learn-langgraph-basics)

Use `ipynb` files to run the notebooks

## Step 2 - Converted them to python code to test on LangGraph Studio

```bash
cd .\01_learn_langgraph_basics\studio\ 

langgraph dev
```

## Step 3 - [Graph API concepts](https://docs.langchain.com/oss/python/graph-api)

Read [Use the graph API](https://docs.langchain.com/oss/python/use-graph-api) as well.

## Step 4 - [Workflows and Agents](https://langchain-ai.github.io/langgraph/tutorials/workflows/)

Watch [YouTube](https://www.youtube.com/watch?v=aHCDrAbH_go) video.

1. Augmented LLMs
2. Prompt chaining
3. Parallelization
4. Routing
5. Orchestrator-worker
6. Evaluator-optimizer
7. Agent coded
8. Agent pre-built

```bash
cd .\02_workflows_and_agents\studio\

langgraph dev
```

## Step 5 - [How to fix your context](https://github.com/langchain-ai/how_to_fix_your_context)

Implemented in python.

1. [Agentic RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
2. Tool loadout
3. Context quarantine
4. Context pruning
5. Context summarization
6. Context offloading

```bash
cd .\03_how_to_fix_your_context\studio\

langgraph dev
```

## Step 6 - [Foundation: Introduction to LangGraph] (https://academy.langchain.com/courses/take/intro-to-langgraph/lessons/58238107-course-overview) by LangChain Academy

See the [Module structure](./04_foundation_introduction_to_langgraph/module_structure.md)
