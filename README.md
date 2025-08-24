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

