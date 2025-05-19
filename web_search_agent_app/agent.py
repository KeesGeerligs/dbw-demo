import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext, FunctionTool
from googlesearch import search

from .prompts import dynamic_instruction_provider, INITIAL_STAGE, PERFORM_SEARCH_STAGE, PRESENT_RESULTS_STAGE

def setup_before_agent_turn(callback_context: CallbackContext) -> None:
    """Initializes essential state variables if they don't exist."""
    if "query_history" not in callback_context.state:
        callback_context.state["query_history"] = []
    if "workflow_stage" not in callback_context.state:
        callback_context.state["workflow_stage"] = INITIAL_STAGE

def _execute_web_search(query: str, num_results: int = 5) -> dict:
    """Performs a Google search using the googlesearch library and returns results."""
    try:
        results = []
        for j in search(query, num_results=num_results):
            results.append(j)
        if not results:
            return {"message": "No search results found."}
        return {"results": results}
    except Exception as e:
        return {"error": f"Error during web search: {str(e)}"}

async def google_search_wrapper_func(query: str, tool_context: ToolContext) -> dict:
    """
    Search the web for information based on the provided query using a custom implementation.
    Manages workflow stage transitions.
    
    Args:
        query: The search query to find information about.
        tool_context: The context for the tool, used for state management.
        
    Returns:
        dict: Search results from the web or an error message.
    """
    current_stage = tool_context.state.get("workflow_stage", INITIAL_STAGE)
    if current_stage == INITIAL_STAGE:
        tool_context.state["workflow_stage"] = PERFORM_SEARCH_STAGE
    
    tool_context.state["current_search_query"] = query
    
    search_results = await asyncio.to_thread(_execute_web_search, query)
    
    tool_context.state["workflow_stage"] = PRESENT_RESULTS_STAGE
    return search_results

def handle_new_message(state: dict, message_text: str) -> dict:
    """
    Updates state based on a new user message.
    Can be called by external app when receiving a message.
    
    Args:
        state: Current session state dictionary
        message_text: The text of the user's message
        
    Returns:
        dict: Updated state dictionary
    """
    current_stage = state.get("workflow_stage", INITIAL_STAGE)
    
    if current_stage == PRESENT_RESULTS_STAGE:
        state["workflow_stage"] = INITIAL_STAGE
    elif current_stage == INITIAL_STAGE and message_text:
        state["workflow_stage"] = PERFORM_SEARCH_STAGE
        state["current_search_query"] = message_text
    
    return state


# Ollama local
api_base_url = "http://localhost:11434"
model_name_at_endpoint = "ollama_chat/mistral-small3.1"

# VLLM
#api_base_url = "https://5pfjqnuugf2pisgegm9ly7pon7xwcsxppx17emweszvf.node.k8s.prd.nos.ci/v1"
#model_name_at_endpoint = "openai/Qwen3-8B"

root_agent = Agent(
    model=LiteLlm(
        model=model_name_at_endpoint,
        api_base=api_base_url,
        api_key="YOUR_ENDPOINT_API_KEY"
    ),
    name="web_search_agent",
    instruction=dynamic_instruction_provider,
    before_agent_callback=setup_before_agent_turn,
    tools=[
        FunctionTool(func=google_search_wrapper_func),
    ],
    description="An agent that can perform web searches based on user queries and present the results.",
)