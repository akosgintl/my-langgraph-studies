"""
Utility functions for LangGraph and LangChain applications.
Includes API key management, structured LLM invoke helpers, and message state utilities.
"""

import os
import json
from typing import Any, Dict, List, Optional, Union, Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig

# Load environment variables from .env file
load_dotenv()


# ============================================================================
# API KEY MANAGEMENT
# ============================================================================

def get_api_key(provider: str, required: bool = True) -> Optional[str]:
    """
    Get API key for a specific provider from environment variables.
    
    Args:
        provider: Provider name (e.g., 'openai', 'anthropic', 'tavily')
        required: Whether the API key is required (raises error if not found)
    
    Returns:
        API key string or None if not found and not required
    
    Raises:
        ValueError: If API key is required but not found
    """
    # Map provider names to environment variable names
    provider_map = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        'tavily': 'TAVILY_API_KEY',
        'google': 'GOOGLE_API_KEY',
        'cohere': 'COHERE_API_KEY',
        'huggingface': 'HUGGINGFACE_API_KEY',
        'mistral': 'MISTRAL_API_KEY',
    }
    
    env_var = provider_map.get(provider.lower())
    if not env_var:
        raise ValueError(f"Unknown provider: {provider}")
    
    api_key = os.environ.get(env_var)
    
    if not api_key and required:
        print(f"{provider.title()} API key not found in environment variables.")
        print(f"Please set {env_var} in your .env file or environment variables.")
        print("You can copy env_example.txt to .env and add your actual API keys.")
        raise ValueError(f"{provider.title()} API key is required. Please check your .env file.")
    
    return api_key


def get_openai_api_key() -> str:
    """Get OpenAI API key from environment variables."""
    return get_api_key('openai')


def get_anthropic_api_key() -> str:
    """Get Anthropic API key from environment variables."""
    return get_api_key('anthropic')


def get_tavily_api_key() -> str:
    """Get Tavily API key from environment variables."""
    return get_api_key('tavily')


def validate_api_keys(providers: List[str]) -> Dict[str, bool]:
    """
    Validate that API keys for specified providers are available.
    
    Args:
        providers: List of provider names to check
    
    Returns:
        Dictionary mapping provider names to availability status
    """
    results = {}
    for provider in providers:
        try:
            get_api_key(provider, required=False)
            results[provider] = True
        except ValueError:
            results[provider] = False
    return results


# ============================================================================
# WORKFLOW UTILITIES
# ============================================================================

def save_workflow_png(workflow, filename: str, directory: Optional[str] = None) -> str:
    """
    Save a workflow graph as a PNG file.
    
    Args:
        workflow: LangGraph workflow object with get_graph() method
        filename: Name of the PNG file (with or without .png extension)
        directory: Directory to save the file in (defaults to caller's directory)
    
    Returns:
        Full path to the saved PNG file
    
    Raises:
        AttributeError: If workflow doesn't have get_graph() method
        ValueError: If filename is invalid
    """
    import inspect
    from pathlib import Path
    
    # Ensure filename has .png extension
    if not filename.lower().endswith('.png'):
        filename += '.png'
    
    # Get the directory of the calling script if not specified
    if directory is None:
        # Get the frame of the calling function
        caller_frame = inspect.currentframe().f_back
        if caller_frame:
            caller_file = caller_frame.f_globals.get('__file__')
            if caller_file:
                directory = str(Path(caller_file).parent)
            else:
                directory = os.getcwd()
        else:
            directory = os.getcwd()
    
    # Create the full file path
    file_path = Path(directory) / filename
    
    try:
        # Get the graph and save as PNG
        graph = workflow.get_graph(xray=True)
        png_data = graph.draw_mermaid_png()
        
        # Save the PNG data to file
        with open(file_path, 'wb') as f:
            f.write(png_data)
        
        print(f"Workflow graph saved to: {file_path}")
        return str(file_path)
        
    except AttributeError:
        raise AttributeError("Workflow object must have a get_graph() method")
    except Exception as e:
        raise ValueError(f"Failed to save workflow graph: {str(e)}")


def save_workflow_mermaid(workflow, filename: str, directory: Optional[str] = None) -> str:
    """
    Save a workflow graph as a Mermaid markdown file.
    
    Args:
        workflow: LangGraph workflow object with get_graph() method
        filename: Name of the markdown file (with or without .md extension)
        directory: Directory to save the file in (defaults to caller's directory)
    
    Returns:
        Full path to the saved markdown file
    
    Raises:
        AttributeError: If workflow doesn't have get_graph() method
        ValueError: If filename is invalid
    """
    import inspect
    from pathlib import Path
    
    # Ensure filename has .md extension
    if not filename.lower().endswith('.md'):
        filename += '.md'
    
    # Get the directory of the calling script if not specified
    if directory is None:
        # Get the frame of the calling function
        caller_frame = inspect.currentframe().f_back
        if caller_frame:
            caller_file = caller_frame.f_globals.get('__file__')
            if caller_file:
                directory = str(Path(caller_file).parent)
            else:
                directory = os.getcwd()
        else:
            directory = os.getcwd()
    
    # Create the full file path
    file_path = Path(directory) / filename
    
    try:
        # Get the graph and save as Mermaid markdown
        graph = workflow.get_graph(xray=True)
        mermaid_code = graph.draw_mermaid()
        
        # Create markdown content with Mermaid code block
        markdown_content = f"""# Workflow Graph

```mermaid
{mermaid_code}
```
"""
        
        # Save the markdown content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Workflow Mermaid saved to: {file_path}")
        return str(file_path)
        
    except AttributeError:
        raise AttributeError("Workflow object must have a get_graph() method")
    except Exception as e:
        raise ValueError(f"Failed to save workflow Mermaid: {str(e)}")
