"""
BlockDAG Network Configuration
"""
from enum import Enum

class NetworkType(Enum):
    MAINNET = 'mainnet'
    TESTNET = 'testnet'
    DEVNET = 'devnet'

# Default configuration
DEFAULT_CONFIG = {
    'network': NetworkType.TESTNET.value,
    'gas_limit': 21000,
    'gas_price': 10,  # in gwei
    'confirmations_required': 6,
    'timeout': 300,  # 5 minutes
}

# API endpoints
ENDPOINTS = {
    NetworkType.MAINNET: 'https://api.blockdag.network/mainnet',
    NetworkType.TESTNET: 'https://api.testnet.blockdag.network',
    NetworkType.DEVNET: 'https://api.devnet.blockdag.network'
}

def get_endpoint(network: NetworkType) -> str:
    """Get API endpoint for the specified network"""
    return ENDPOINTS.get(network, ENDPOINTS[NetworkType.TESTNET])
