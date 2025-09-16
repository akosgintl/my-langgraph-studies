# Tutorials

**NOTE**: The original was mdx, converted to md. Based on [this](https://github.com/langchain-ai/langchain/tree/master/docs/docs/tutorials)

New to LangChain or LLM app development in general? Read this material to quickly get up and running building your first applications.

## Get started

Familiarize yourself with LangChain's open-source components by building simple applications.

If you're looking to get started with [chat models](https://github.com/langchain-ai/langchain/tree/master/docs/docs/integrations/chat/), [vector stores](https://github.com/langchain-ai/langchain/tree/master/docs/docs/integrations/vectorstores/),
or other LangChain components from a specific provider, check out our supported [integrations](https://github.com/langchain-ai/langchain/tree/master/docs/docs/integrations/providers/).

- [Chat models and prompts](llm_chain.ipynb): Build a simple LLM application with [prompt templates](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/prompt_templates) and [chat models](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/chat_models).
- [Semantic search](retrievers.ipynb): Build a semantic search engine over a PDF with [document loaders](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/document_loaders), [embedding models](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/embedding_models/), and [vector stores](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/vectorstores/).
- [Classification](classification.ipynb): Classify text into categories or labels using [chat models](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/chat_models) with [structured outputs](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/structured_outputs/).
- [Extraction](extraction.ipynb): Extract structured data from text and other unstructured media using [chat models](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/chat_models) and [few-shot examples](https://github.com/langchain-ai/langchain/tree/master/docs/docs/concepts/few_shot_prompting/).

Refer to the [how-to guides](https://github.com/langchain-ai/langchain/tree/master/docs/docs/how_to) for more detail on using all LangChain components.

## Orchestration

Get started using [LangGraph](https://langchain-ai.github.io/langgraph/) to assemble LangChain components into full-featured applications.

- [Chatbots](chatbot.ipynb): Build a chatbot that incorporates memory.
- [Agents](agents.ipynb): Build an agent that interacts with external tools.
- [Retrieval Augmented Generation (RAG) Part 1](rag.ipynb): Build an application that uses your own documents to inform its responses.
- [Retrieval Augmented Generation (RAG) Part 2](qa_chat_history.ipynb): Build a RAG application that incorporates a memory of its user interactions and multi-step retrieval.
- [Question-Answering with SQL](sql_qa.ipynb): Build a question-answering system that executes SQL queries to inform its responses.
- [Summarization](summarization.ipynb): Generate summaries of (potentially long) texts.
- [Question-Answering with Graph Databases](graph.ipynb): Build a question-answering system that queries a graph database to inform its responses.

## LangSmith

LangSmith allows you to closely trace, monitor and evaluate your LLM application.
It seamlessly integrates with LangChain, and you can use it to inspect and debug individual steps of your chains as you build.

LangSmith documentation is hosted on a separate site.
You can peruse [LangSmith tutorials here](https://docs.smith.langchain.com/).

### Evaluation

LangSmith helps you evaluate the performance of your LLM applications. The tutorial below is a great way to get started:

- [Evaluate your LLM application](https://docs.smith.langchain.com/tutorials/Developers/evaluation)
