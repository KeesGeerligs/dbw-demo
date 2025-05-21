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

"""Transaction Analysis Agent for examining blockchain transaction patterns."""

from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm
from typing import Dict, Any, Union

from blockchain_security.config import API_BASE_URL, MODEL_NAME_AT_ENDPOINT, API_KEY
from blockchain_security.tools.transaction_data import transaction_data_tool
from . import prompt

def analyze_transactions(input_value: str) -> Dict[str, Any]:
    """
    Analyze blockchain transactions for suspicious patterns.
    
    Args:
        input_value: Either a blockchain address or a transaction hash
        
    Returns:
        Dictionary with transaction analysis results
    """
    # Check if input is a transaction hash (simplified check for demo)
    if input_value.startswith("0x") and len(input_value) >= 64:
        # Analyze a specific transaction
        transaction = transaction_data_tool.get_transaction_by_hash(input_value)
        
        # For a real implementation, this would include more detailed analysis
        # of the specific transaction
        
        return {
            "transaction_hash": input_value,
            "transaction_details": transaction,
            "analysis_type": "single_transaction"
        }
    else:
        # Assume it's an address and analyze its transaction patterns
        transaction_patterns = transaction_data_tool.analyze_transaction_patterns(input_value)
        transactions = transaction_data_tool.get_transactions_by_address(input_value)
        
        return {
            "address": input_value,
            "transaction_patterns": transaction_patterns,
            "transactions": transactions,
            "analysis_type": "address_transactions"
        }

transaction_analysis_agent = Agent(
    model=LiteLlm(
        model=MODEL_NAME_AT_ENDPOINT,
        api_base=API_BASE_URL,
        api_key=API_KEY
    ),
    name="transaction_analysis_agent",
    description="Examines blockchain transaction patterns to identify suspicious activities",
    instruction=prompt.TRANSACTION_ANALYSIS_PROMPT,
    tools=[
        FunctionTool(
            func=analyze_transactions,
        )
    ]
)
