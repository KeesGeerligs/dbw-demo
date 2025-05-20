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

"""Risk score API tool for blockchain security."""

from typing import Dict, Any, List
from . import blockchain_data
from .address_lookup import address_lookup_tool
from .transaction_data import transaction_data_tool

class RiskScoreAPI:
    """Tool for calculating risk scores for blockchain addresses."""
    
    @staticmethod
    def get_risk_score(address: str) -> Dict[str, Any]:
        """
        Calculate a risk score for an address based on various factors.
        
        Args:
            address: The blockchain address to analyze
            
        Returns:
            Dictionary with risk score and justification
        """
        # Check if address is a known scammer
        scam_status = address_lookup_tool.check_scam_status(address)
        
        if scam_status.get("is_scam", False):
            return {
                "address": address,
                "risk_score": scam_status["details"]["risk_score"],
                "risk_level": "High",
                "justification": f"Known {scam_status['details']['scam_type']} scam address reported by {', '.join(scam_status['details']['reported_by'])}",
                "details": scam_status["details"]
            }
        
        # Check if address is connected to known scammers
        if scam_status.get("is_connected_to_scam", False):
            return {
                "address": address,
                "risk_score": 0.7,  # High but not as high as direct scammer
                "risk_level": "High",
                "justification": f"Connected to known {scam_status['scam_details']['scam_type']} scam address",
                "details": {
                    "connected_scam_address": scam_status["connected_scam_address"],
                    "scam_details": scam_status["scam_details"]
                }
            }
        
        # Check for suspicious transaction patterns
        transaction_analysis = transaction_data_tool.analyze_transaction_patterns(address)
        
        risk_factors = []
        max_risk_score = 0.0
        
        for pattern in transaction_analysis.get("detected_patterns", []):
            risk_factors.append({
                "factor": pattern["pattern"],
                "description": pattern["description"],
                "risk_score": pattern["risk_score"]
            })
            max_risk_score = max(max_risk_score, pattern["risk_score"])
        
        # Check wallet behavioral patterns
        wallet_data = address_lookup_tool.get_address_details(address).get("wallet_data", {})
        
        # If we have the wallet in our sample data, use its risk score
        if wallet_data:
            wallet_risk_score = wallet_data.get("risk_score", 0.0)
            if wallet_risk_score > max_risk_score:
                max_risk_score = wallet_risk_score
                risk_factors.append({
                    "factor": "historical_behavior",
                    "description": "Historical wallet behavior indicates risk",
                    "risk_score": wallet_risk_score
                })
        
        # Determine risk level
        risk_level = "Low"
        if max_risk_score >= 0.8:
            risk_level = "High"
        elif max_risk_score >= 0.5:
            risk_level = "Medium"
        
        # Generate justification
        justification = "No significant risk factors detected"
        if risk_factors:
            factor_descriptions = [f"{factor['description']} (score: {factor['risk_score']})" 
                                  for factor in risk_factors]
            justification = f"Risk factors detected: {'; '.join(factor_descriptions)}"
        
        return {
            "address": address,
            "risk_score": max_risk_score,
            "risk_level": risk_level,
            "justification": justification,
            "details": {
                "risk_factors": risk_factors,
                "transaction_analysis": transaction_analysis
            }
        }
    
    @staticmethod
    def analyze_behavioral_patterns(address: str) -> Dict[str, Any]:
        """
        Analyze behavioral patterns for an address.
        
        Args:
            address: The blockchain address to analyze
            
        Returns:
            Dictionary with behavior analysis
        """
        # Get transaction data
        transactions = transaction_data_tool.get_transactions_by_address(address)
        
        # Check for patterns in our behavioral database
        detected_patterns = []
        
        # Example pattern check: excessive minting
        # In a real implementation, this would analyze actual transaction data
        # For this simulation, we'll randomly assign some patterns based on address
        if address.startswith("0x2222"):
            detected_patterns.append({
                "pattern": "dump_cycle",
                **blockchain_data.WALLET_BEHAVIORAL_PATTERNS["dump_cycle"]
            })
        
        if address.startswith("0x3333"):
            detected_patterns.append({
                "pattern": "excessive_minting",
                **blockchain_data.WALLET_BEHAVIORAL_PATTERNS["excessive_minting"]
            })
        
        return {
            "address": address,
            "transaction_count": len(transactions),
            "detected_patterns": detected_patterns,
            "risk_assessment": len(detected_patterns) > 0
        }

# Initialize the tool
risk_score_api = RiskScoreAPI()
