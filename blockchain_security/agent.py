# Copyright 2025
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

"""Blockchain Security Coordinator Agent assists in identifying and mitigating blockchain security threats."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from google.adk.models.lite_llm import LiteLlm
from .sub_agents.scam_detection import scam_detection_agent
from .sub_agents.risk_classification import risk_classification_agent
from .sub_agents.transaction_analysis import transaction_analysis_agent
from .config import API_BASE_URL, MODEL_NAME_AT_ENDPOINT, API_KEY

blockchain_security_coordinator = LlmAgent(
    name="blockchain_security_coordinator",
    model=LiteLlm(
        model=MODEL_NAME_AT_ENDPOINT,
        api_base=API_BASE_URL,
        api_key=API_KEY
    ),
    description=(
        "Protect your blockchain assets and interactions by detecting security threats "
        "and vulnerabilities. Analyze addresses for known scam patterns, classify wallet "
        "addresses based on risk profiles, and examine transaction patterns for suspicious "
        "activities. Empower users to make safer blockchain interactions through AI-powered "
        "security analysis and alerts."
    ),
    instruction=prompt.SECURITY_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=scam_detection_agent),
        AgentTool(agent=risk_classification_agent),
        AgentTool(agent=transaction_analysis_agent),
    ],
)

root_agent = blockchain_security_coordinator
