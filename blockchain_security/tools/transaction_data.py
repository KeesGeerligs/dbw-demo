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

"""Transaction data tool for blockchain security."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from . import blockchain_data

class TransactionData:
    """Tool for analyzing blockchain transaction data."""
    
    @staticmethod
    def get_transaction_by_hash(tx_hash: str) -> Dict[str, Any]:
        """
        Get transaction data by transaction hash.
        
        Args:
            tx_hash: The transaction hash to look up
            
        Returns:
            Dictionary with transaction details
        """
        if tx_hash in blockchain_data.SAMPLE_TRANSACTIONS:
            return {
                "hash": tx_hash,
                **blockchain_data.SAMPLE_TRANSACTIONS[tx_hash]
            }
        
        return {
            "error": "Transaction not found",
            "hash": tx_hash
        }
    
    @staticmethod
    def get_transactions_by_address(address: str) -> List[Dict[str, Any]]:
        """
        Get transactions related to an address.
        
        Args:
            address: The blockchain address to find transactions for
            
        Returns:
            List of transaction details
        """
        transactions = []
        for tx_hash, tx_data in blockchain_data.SAMPLE_TRANSACTIONS.items():
            if tx_data["from"] == address or tx_data["to"] == address:
                transactions.append({
                    "hash": tx_hash,
                    **tx_data
                })
        
        return transactions
    
    @staticmethod
    def analyze_transaction_patterns(address: str) -> Dict[str, Any]:
        """
        Analyze transaction patterns for an address.
        
        Args:
            address: The blockchain address to analyze
            
        Returns:
            Dictionary with pattern analysis
        """
        transactions = TransactionData.get_transactions_by_address(address)
        
        # Check for rapid transfers
        tx_timestamps = [datetime.fromisoformat(tx["timestamp"].replace("Z", "+00:00")) 
                         for tx in transactions]
        tx_timestamps.sort()
        
        rapid_transfers = False
        for i in range(1, len(tx_timestamps)):
            time_diff = (tx_timestamps[i] - tx_timestamps[i-1]).total_seconds()
            if time_diff < 60:  # Less than a minute between transactions
                rapid_transfers = True
                break
        
        # Check if address interacts with known scam addresses
        interacts_with_scammers = False
        scam_interactions = []
        
        for tx in transactions:
            if tx["from"] in blockchain_data.KNOWN_SCAM_ADDRESSES:
                interacts_with_scammers = True
                scam_interactions.append({
                    "tx_hash": tx.get("hash", ""),
                    "scam_address": tx["from"],
                    "scam_type": blockchain_data.KNOWN_SCAM_ADDRESSES[tx["from"]]["scam_type"]
                })
            
            if tx["to"] in blockchain_data.KNOWN_SCAM_ADDRESSES:
                interacts_with_scammers = True
                scam_interactions.append({
                    "tx_hash": tx.get("hash", ""),
                    "scam_address": tx["to"],
                    "scam_type": blockchain_data.KNOWN_SCAM_ADDRESSES[tx["to"]]["scam_type"]
                })
        
        # Determine overall risk pattern
        detected_patterns = []
        if rapid_transfers:
            detected_patterns.append({
                "pattern": "rapid_transfers",
                **blockchain_data.SUSPICIOUS_TRANSACTION_PATTERNS["rapid_transfers"]
            })
        
        if interacts_with_scammers:
            detected_patterns.append({
                "pattern": "scam_interaction",
                "description": "Interaction with known scam addresses",
                "risk_score": 0.80,
                "details": scam_interactions
            })
        
        return {
            "address": address,
            "transaction_count": len(transactions),
            "detected_patterns": detected_patterns,
            "risk_assessment": len(detected_patterns) > 0
        }

# Initialize the tool
transaction_data_tool = TransactionData()
