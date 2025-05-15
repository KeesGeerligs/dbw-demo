# Web Search Agent Setup Guide

This guide explains how to set up and run the Web Search Agent application.

## Setting up the Web Search Agent

First, install Ollama from [https://ollama.com/](https://ollama.com/) and ensure it is running.

Next, pull the required language model via your terminal:
```bash
ollama pull mistral-small3.1
```

Then, install the Python dependencies for the agent:
```bash
pip install -r requirements.txt
```

Finally, run the agent application using the ADK web interface:
```bash
adk web
```
If your Ollama server is not running at `http://localhost:11434`, you will need to set the `OLLAMA_API_BASE` environment variable to the correct address before running `adk web`.

Once `adk web` is active, open your browser to the displayed URL `http://localhost:8000`

## Using a Non-Local Endpoint (Nosana)

Alternatively, you can use a non-local model endpoint by deploying the provided `job-definition.json` on the Nosana network.

1.  **Deploy the Job:**
    *   Use the Nosana CLI or dashboard to deploy the `job-definition.json` file. This will provision a VLLM instance running the Qwen3-8B model.
2.  **Obtain the Endpoint URL:**
    *   Once deployed, Nosana will provide you with a URL for your running job. This URL will serve as the `api_base_url`.
3.  **Update Agent Configuration:**
    *   In `web_search_agent_app/agent.py`, modify the `api_base_url` and `model_name_at_endpoint` variables to match your Nosana deployment:
        ```python
        # VLLM (example for Nosana)
        api_base_url = "YOUR_NOSANA_ENDPOINT_URL/v1" 
        model_name_at_endpoint = "openai/Qwen3-8B" # Or the specific model served by your job
        ```
    *   Ensure you also set the `api_key` if required by your endpoint (for Nosana's VLLM OpenAI-compatible endpoint, an API key is often not strictly needed but might be configurable).
4.  **Run the Agent:**
    *   After updating the agent configuration, run `adk web` as usual. The agent will now use your deployed Nosana endpoint.

This method allows you to use more powerful models without needing local GPU resources, leveraging the decentralized compute power of the Nosana network.
