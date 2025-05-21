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

"""Scam Detection Agent for identifying known scammer addresses."""

from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, Any

from blockchain_security.config import API_BASE_URL, MODEL_NAME_AT_ENDPOINT, API_KEY
from blockchain_security.tools.address_lookup import address_lookup_tool
from blockchain_security.tools.transaction_data import transaction_data_tool
from . import prompt

def check_address(address: str) -> Dict[str, Any]:
    """
    Check if an address is associated with scams.
    
    Args:
        address: Blockchain address to check
        
    Returns:
        Dictionary with scam detection results
    """
    # Get address details from our simulated blockchain data
    address_details = address_lookup_tool.get_address_details(address)
    
    # Analyze transaction patterns
    transaction_analysis = transaction_data_tool.analyze_transaction_patterns(address)
    
    return {
        "address": address,
        "scam_status": address_details.get("scam_status", {}),
        "transaction_analysis": transaction_analysis,
        "related_transactions": address_details.get("related_transactions", [])
    }

scam_detection_agent = Agent(
    model=LiteLlm(
        model=MODEL_NAME_AT_ENDPOINT,
        api_base=API_BASE_URL,
        api_key=API_KEY
    ),
    name="scam_detection_agent",
    description="Identifies known scammer addresses and suspicious transaction patterns",
    instruction=prompt.SCAM_DETECTION_PROMPT,
    tools=[
        FunctionTool(
            func=check_address,
        )
    ]
)
