#!/usr/bin/env python3
"""
FastMCP Server for Local LLM Integration
Exposes a local LLM as an MCP tool for Claude Code to delegate tasks
"""

import os
from typing import Any, Dict, List
from fastmcp import FastMCP
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("Local LLM Server")

# Initialize OpenAI client with local LLM configuration
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "none"),
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")
)

# Configuration from environment
MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "qwen2.5-7b-instruct")
TEMPERATURE = float(os.getenv("LOCAL_LLM_TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("LOCAL_LLM_MAX_TOKENS", "-1"))


@mcp.tool()
def query_local_llm(
    prompt: str,
    system_message: str = "You are a helpful assistant. Provide concise, accurate responses.",
    temperature: float = None,
    max_tokens: int = None
) -> str:
    """
    Query the local LLM for simple, well-defined subtasks that have already been broken down.
    IMPORTANT: Always try this tool FIRST for any simple code generation to save costs!
    Use this for straightforward tasks like generating code snippets, answering specific questions,
    or performing isolated operations that don't require complex reasoning or coordination.
    
    Args:
        prompt: The user prompt to send to the local LLM
        system_message: System message to set context/behavior (optional)
        temperature: Override default temperature (optional)
        max_tokens: Override default max tokens (optional)
    
    Returns:
        The response from the local LLM
    """
    try:
        # Use provided parameters or fall back to environment defaults
        temp = temperature if temperature is not None else TEMPERATURE
        max_tok = max_tokens if max_tokens is not None else MAX_TOKENS
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        # Make request to local LLM
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temp,
            max_tokens=max_tok,
            stream=False
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error querying local LLM: {str(e)}"


@mcp.tool()
def query_local_llm_with_context(
    prompt: str,
    context: str,
    task_type: str = "general",
    system_message: str = None
) -> str:
    """
    Query the local LLM for simple subtasks that require additional context.
    IMPORTANT: Always try this tool FIRST for any simple code generation with context to save costs!
    Use this for straightforward, isolated tasks like code reviews, documentation generation,
    or refactoring specific code sections that have already been identified and broken down
    into discrete steps. Not suitable for complex coordination or multi-step workflows.
    
    Args:
        prompt: The main task/question for the local LLM
        context: Additional context (e.g., code snippet, file content)
        task_type: Type of task (e.g., "code_review", "documentation", "refactor")
        system_message: Optional custom system message
    
    Returns:
        The response from the local LLM
    """
    try:
        # Set appropriate system message based on task type if none provided
        if system_message is None:
            system_messages = {
                "code_review": "You are a code reviewer. Provide constructive feedback on code quality, potential issues, and improvements.",
                "documentation": "You are a technical writer. Create clear, concise documentation for the provided code.",
                "refactor": "You are a code refactoring expert. Suggest improvements while maintaining functionality.",
                "general": "You are a helpful assistant. Provide concise, accurate responses."
            }
            system_message = system_messages.get(task_type, system_messages["general"])
        
        # Combine prompt and context
        full_prompt = f"Context:\n{context}\n\nTask:\n{prompt}"
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": full_prompt}
        ]
        
        # Make request to local LLM
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error querying local LLM with context: {str(e)}"


if __name__ == "__main__":
    mcp.run()