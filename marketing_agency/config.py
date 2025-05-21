# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared configuration settings for marketing agency agents"""

# Model API settings
# -----------------

# VLLM (Production)
VLLM_API_BASE_URL = "https://ejesl8ljrjmjvrwalhflzkzszgfqqkd7153vcr33cura.node.k8s.prd.nos.ci/v1"
VLLM_MODEL_NAME = "openai/Qwen3-8B"

# Ollama (Local Development)
OLLAMA_API_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL_NAME = "ollama_chat/mistral-small3.1"

# Default settings
# ---------------
# Set these variables to choose which configuration to use
# Change to OLLAMA_* variables for local development

API_BASE_URL = OLLAMA_API_BASE_URL
MODEL_NAME_AT_ENDPOINT = OLLAMA_MODEL_NAME

# Default API key - override this in your agent if needed
API_KEY = "YOUR_ENDPOINT_API_KEY"
