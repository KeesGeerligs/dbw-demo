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

"""Risk Classification Agent for predictive wallet analysis."""

from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, Any

from blockchain_security.config import API_BASE_URL, MODEL_NAME_AT_ENDPOINT, API_KEY
from blockchain_security.tools.risk_score_api import risk_score_api
from . import prompt

def classify_risk(address: str) -> Dict[str, Any]:
    """
    Classify the risk level of a blockchain address.
    
    Args:
        address: Blockchain address to classify
        
    Returns:
        Dictionary with risk classification results
    """
    # Get risk score from our simulated API
    risk_assessment = risk_score_api.get_risk_score(address)
    
    # Get behavioral patterns analysis
    behavior_analysis = risk_score_api.analyze_behavioral_patterns(address)
    
    return {
        "address": address,
        "risk_assessment": risk_assessment,
        "behavior_analysis": behavior_analysis
    }

risk_classification_agent = Agent(
    model=LiteLlm(
        model=MODEL_NAME_AT_ENDPOINT,
        api_base=API_BASE_URL,
        api_key=API_KEY
    ),
    name="risk_classification_agent",
    description="Performs predictive network analysis to classify wallet addresses based on behavioral risk patterns",
    instruction=prompt.RISK_CLASSIFICATION_PROMPT,
    tools=[
        FunctionTool(
            func=classify_risk
        )
    ]
)
