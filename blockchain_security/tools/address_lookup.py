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

"""Address lookup tool for blockchain security."""

from typing import Dict, Any, List, Optional
from . import blockchain_data

class AddressLookup:
    """Tool for looking up address information from simulated blockchain data."""
    
    @staticmethod
    def check_scam_status(address: str) -> Dict[str, Any]:
        """
        Check if an address is in the known scammer database.
        
        Args:
            address: The blockchain address to check
            
        Returns:
            Dictionary with scam status information
        """
        if address in blockchain_data.KNOWN_SCAM_ADDRESSES:
            return {
                "is_scam": True,
                "details": blockchain_data.KNOWN_SCAM_ADDRESSES[address]
            }
        
        # Check for connection to known scam addresses
        for wallet_address, wallet_data in blockchain_data.SAMPLE_WALLETS.items():
            if address == wallet_address:
                for connected_address in wallet_data.get("connected_addresses", []):
                    if connected_address in blockchain_data.KNOWN_SCAM_ADDRESSES:
                        return {
                            "is_scam": False,
                            "is_connected_to_scam": True,
                            "connected_scam_address": connected_address,
                            "scam_details": blockchain_data.KNOWN_SCAM_ADDRESSES[connected_address]
                        }
        
        return {
            "is_scam": False,
            "is_connected_to_scam": False
        }
    
    @staticmethod
    def get_address_details(address: str) -> Dict[str, Any]:
        """
        Get detailed information about an address.
        
        Args:
            address: The blockchain address to look up
            
        Returns:
            Dictionary with address details
        """
        # Check if we have this address in our sample wallet data
        wallet_data = blockchain_data.SAMPLE_WALLETS.get(address, {})
        scam_status = AddressLookup.check_scam_status(address)
        
        # Get transactions related to this address
        related_transactions = []
        for tx_hash, tx_data in blockchain_data.SAMPLE_TRANSACTIONS.items():
            if tx_data["from"] == address or tx_data["to"] == address:
                related_transactions.append({
                    "hash": tx_hash,
                    **tx_data
                })
        
        return {
            "address": address,
            "wallet_data": wallet_data,
            "scam_status": scam_status,
            "related_transactions": related_transactions
        }
    
    @staticmethod
    def get_connected_addresses(address: str) -> List[str]:
        """
        Get addresses connected to the given address.
        
        Args:
            address: The blockchain address to find connections for
            
        Returns:
            List of connected addresses
        """
        wallet_data = blockchain_data.SAMPLE_WALLETS.get(address, {})
        return wallet_data.get("connected_addresses", [])

# Initialize the tool
address_lookup_tool = AddressLookup()
