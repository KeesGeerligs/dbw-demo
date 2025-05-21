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

"""Static blockchain data for simulation."""

# Known scam addresses for demonstration
KNOWN_SCAM_ADDRESSES = {
    "0x1234abcd5678efgh9012ijkl3456mnop7890qrst": {
        "scam_type": "phishing",
        "risk_score": 0.95,
        "reported_by": ["Chainalysis", "Etherscan"],
        "first_reported": "2025-01-15",
        "description": "Known phishing address targeting DeFi users"
    },
    "0xabcd1234efgh5678ijkl9012mnop3456qrst7890": {
        "scam_type": "rug_pull",
        "risk_score": 0.90,
        "reported_by": ["ScamSniffer", "De.Fi"],
        "first_reported": "2025-02-20",
        "description": "Associated with rug pull of TokenXYZ project"
    },
    "0x5678abcd1234efgh9012ijkl3456mnop7890qrst": {
        "scam_type": "mixer",
        "risk_score": 0.85,
        "reported_by": ["SlowMist"],
        "first_reported": "2025-03-10",
        "description": "Frequently used for laundering funds through mixers"
    }
}

# Sample transaction patterns for demonstration
SUSPICIOUS_TRANSACTION_PATTERNS = {
    "rapid_transfers": {
        "description": "Multiple high-value transfers in short time period",
        "risk_score": 0.75,
        "indicators": ["Multiple transactions within minutes", "High ETH/token values", "Destination is exchange or mixer"]
    },
    "token_honeypot": {
        "description": "Token contract prevents selling by normal users",
        "risk_score": 0.85,
        "indicators": ["Custom token contract", "Only creator can sell", "Liquidity locked or removed after launch"]
    },
    "chain_hopping": {
        "description": "Funds moved across multiple blockchains quickly",
        "risk_score": 0.70,
        "indicators": ["Use of cross-chain bridges", "Immediate withdrawal on destination chain", "Final destination is typically exchange"]
    }
}

# Sample wallet behavioral patterns
WALLET_BEHAVIORAL_PATTERNS = {
    "excessive_minting": {
        "description": "Wallet creates excessive amounts of new tokens",
        "risk_score": 0.65,
        "indicators": ["Multiple token creation transactions", "Similar token contracts", "Low liquidity provision"]
    },
    "dump_cycle": {
        "description": "Pattern of accumulating tokens then selling quickly",
        "risk_score": 0.80,
        "indicators": ["Accumulation phase", "Rapid selling phase", "Repeated pattern across multiple tokens"]
    },
    "wash_trading": {
        "description": "Self-trading to create fake volume",
        "risk_score": 0.75,
        "indicators": ["Trading between related wallets", "Circular transaction patterns", "Artificially inflated volumes"]
    }
}

# Sample transaction data
SAMPLE_TRANSACTIONS = {
    "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890": {
        "from": "0x1111aaaa2222bbbb3333cccc4444dddd5555eeee",
        "to": "0x1234abcd5678efgh9012ijkl3456mnop7890qrst",  # known scam address
        "value": "5.2 ETH",
        "timestamp": "2025-05-10T14:32:15Z",
        "gas_used": 21000,
        "status": "success"
    },
    "0x0987654321fedcba0987654321fedcba0987654321fedcba0987654321fedcba": {
        "from": "0x6666ffff7777gggg8888hhhh9999iiii0000jjjj",
        "to": "0x2222bbbb3333cccc4444dddd5555eeee6666ffff",
        "value": "10000 USDT",
        "timestamp": "2025-05-10T14:35:22Z",
        "gas_used": 65000,
        "status": "success"
    },
    "0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321": {
        "from": "0x2222bbbb3333cccc4444dddd5555eeee6666ffff",
        "to": "0xabcd1234efgh5678ijkl9012mnop3456qrst7890",  # known scam address
        "value": "10000 USDT",
        "timestamp": "2025-05-10T14:36:05Z",
        "gas_used": 65000,
        "status": "success"
    }
}

# Sample wallet data
SAMPLE_WALLETS = {
    "0x1111aaaa2222bbbb3333cccc4444dddd5555eeee": {
        "creation_date": "2024-12-01",
        "total_transactions": 152,
        "current_balance": {
            "ETH": "12.5",
            "USDT": "5000",
            "USDC": "3000"
        },
        "risk_score": 0.15,
        "connected_addresses": [
            "0x2222bbbb3333cccc4444dddd5555eeee6666ffff",
            "0x3333cccc4444dddd5555eeee6666ffff7777gggg"
        ]
    },
    "0x2222bbbb3333cccc4444dddd5555eeee6666ffff": {
        "creation_date": "2025-01-15",
        "total_transactions": 27,
        "current_balance": {
            "ETH": "0.5",
            "USDT": "0",
            "USDC": "100"
        },
        "risk_score": 0.75,
        "connected_addresses": [
            "0x1111aaaa2222bbbb3333cccc4444dddd5555eeee",
            "0xabcd1234efgh5678ijkl9012mnop3456qrst7890"  # connected to known scam address
        ]
    },
    "0x3333cccc4444dddd5555eeee6666ffff7777gggg": {
        "creation_date": "2024-09-10",
        "total_transactions": 342,
        "current_balance": {
            "ETH": "45.2",
            "USDT": "12000",
            "USDC": "8000"
        },
        "risk_score": 0.05,
        "connected_addresses": [
            "0x1111aaaa2222bbbb3333cccc4444dddd5555eeee",
            "0x4444dddd5555eeee6666ffff7777gggg8888hhhh"
        ]
    }
}
