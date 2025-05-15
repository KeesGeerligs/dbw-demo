import os
import asyncio # Added for asyncio.to_thread
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext, FunctionTool
from googlesearch import search # Added for custom search

# Import prompts and tools
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
        # The search function from googlesearch is a generator
        for j in search(query, num_results=num_results):
            results.append(j)
        if not results:
            return {"message": "No search results found."}
        return {"results": results} # Returns a list of URLs
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
        # If called in initial stage, means user provided query, advance stage
        tool_context.state["workflow_stage"] = PERFORM_SEARCH_STAGE
    
    tool_context.state["current_search_query"] = query
    
    # Call the synchronous custom search function in a separate thread
    search_results = await asyncio.to_thread(_execute_web_search, query)
    
    tool_context.state["workflow_stage"] = PRESENT_RESULTS_STAGE
    return search_results

# Define the agent
# ADK CLI typically looks for an agent instance named 'agent' or 'root_agent'.
# Renaming to root_agent for ADK CLI discovery.
root_agent = Agent(
    model=LiteLlm(model='ollama_chat/mistral-small3.1'),
    name="web_search_agent", # This name is for the agent's identity, not the variable name
    instruction=dynamic_instruction_provider,
    before_agent_callback=setup_before_agent_turn, # Changed to before_agent_callback
    tools=[
        FunctionTool(func=google_search_wrapper_func),
    ],
    description="An agent that can perform web searches based on user queries and present the results.",
)

# Handle messages directly to transition stages when needed
# This function can be used by an external app to transition the stage based on new user input
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
        # If we're in PRESENT_RESULTS and get a new message, go back to INITIAL
        state["workflow_stage"] = INITIAL_STAGE
    elif current_stage == INITIAL_STAGE and message_text:
        # If we're in INITIAL and get a message that's not empty, prepare for search
        state["workflow_stage"] = PERFORM_SEARCH_STAGE
        state["current_search_query"] = message_text
    
    return state

# Removed the if __name__ == "__main__": block and InteractiveRunner
# The agent instance above will be picked up by `adk run <folder_name>` 