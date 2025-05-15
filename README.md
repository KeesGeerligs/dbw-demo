# Web Search Agent using Google ADK

This project implements a simple web search agent using the Google Agent Development Kit (ADK).
The agent interacts with the user to get a search query, performs a web search, and then presents the results.

## Features

- Conversational interface to get search queries.
- Uses Google ADK for agent framework.
- Employs LiteLLM with `ollama_chat/mistral-small3.1` for language understanding and response generation.
- Workflow-based interaction: `get_search_query` -> `perform_web_search` -> `present_search_results`.
- Uses ADK's built-in `google_search` tool.

## Project Structure

- `web_search_agent_app/`
  - `__init__.py`: Makes the folder a Python package.
  - `agent.py`: Contains the main agent definition, workflow logic, and tool integration.
  - `prompts.py`: Provides dynamic instructions to the agent based on the current stage of the workflow.
- `requirements.txt`: Lists the Python dependencies for the project.
- `README.md`: This file.

## Prerequisites

- Python 3.8 or higher.
- Pip (Python package installer).
- Google ADK installed (`pip install google-adk`).
- An Ollama server running with the `mistral-small3.1` model pulled. 
  - Install Ollama: [https://ollama.com/](https://ollama.com/)
  - Pull the model: `ollama pull mistral-small3.1`
- Potentially, a Google Search API key if the `google_search` tool requires it. This depends on the ADK's implementation of the tool and might require setting environment variables like `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`.

## Setup

1.  **Clone the repository (if applicable) or create the files and folder structure as listed above.**

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ensure Ollama is running and the model is available.**
    By default, LiteLLM will try to connect to Ollama at `http://localhost:11434`.
    If your Ollama server is running elsewhere, you might need to set the `OLLAMA_API_BASE` environment variable:
    ```bash
    export OLLAMA_API_BASE="http://your-ollama-host:port"
    ```

## Running the Agent

To run the agent, navigate to the root directory of the project (the one containing the `web_search_agent_app` folder and `requirements.txt`) and use the ADK CLI:

```bash
adk run web_search_agent_app
```

This will start the ADK web interface (usually on `http://localhost:8000`) where you can interact with the agent.

## How it Works

1.  The `adk run web_search_agent_app` command discovers the `agent` instance in `web_search_agent_app/agent.py`.
2.  The `agent` is initialized with a LiteLLM model (`ollama_chat/mistral-small3.1`).
3.  The `before_agent_turn_callback` (`setup_before_agent_call`) function manages the `workflow_stage` in the agent's state.
4.  The `dynamic_instruction_provider` from `prompts.py` supplies the LLM with instructions based on the current `workflow_stage`.
5.  **Stage 1: `get_search_query`**: The agent asks the user for a search query.
6.  **Stage 2: `perform_web_search`**: Once the query is received, the state transitions. The LLM, guided by the prompts, is instructed to use the `google_search` tool with the user's query.
7.  **Stage 3: `present_search_results`**: The agent receives the output from the `google_search` tool and presents it to the user. It then asks if the user needs further assistance.

## Customization

-   **LLM Model**: You can change the LLM model by modifying the `model` parameter in the `Agent` definition in `agent.py` (ensure LiteLLM supports it).
-   **Prompts**: The agent's behavior and responses can be fine-tuned by editing the instructions in `prompts.py`.
-   **Tools**: Additional tools can be added to the agent by defining them and including them in the `tools` list in `agent.py`. 