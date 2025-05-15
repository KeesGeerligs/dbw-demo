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
