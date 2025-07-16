"""
BlockDAG Network Wallet Integration for OSCARR
Handles BDAG transactions and wallet operations
"""
import os
from dotenv import load_dotenv
from blockdag_network_sdk import BlockDAGClient
from typing import Dict, List, Optional
import json

class BlockDAGWallet:
    def __init__(self, network: str = 'testnet'):
        """Initialize BlockDAG wallet with API credentials"""
        load_dotenv()
        self.network = network
        self.client = self._initialize_client()
        
    def _initialize_client(self) -> BlockDAGClient:
        """Initialize BlockDAG client with environment variables"""
        api_key = os.getenv('BLOCKDAG_API_KEY')
        if not api_key:
            raise ValueError("BLOCKDAG_API_KEY not found in environment variables")
        return BlockDAGClient(api_key=api_key, network=self.network)
    
    def get_balance(self, address: str = None) -> Dict:
        """Get balance for a specific address or the default wallet"""
        if not address:
            address = os.getenv('BLOCKDAG_WALLET_ADDRESS')
        return self.client.get_balance(address)
    
    def send_transaction(
        self, 
        to_address: str, 
        amount: float, 
        asset: str = 'BDAG',
        private_key: str = None
    ) -> Dict:
        """
        Send BDAG or other supported assets
        
        Args:
            to_address: Recipient's BDAG address
            amount: Amount to send
            asset: Asset type (default: BDAG)
            private_key: Sender's private key (if not using env var)
            
        Returns:
            Transaction receipt
        """
        if not private_key:
            private_key = os.getenv('BLOCKDAG_PRIVATE_KEY')
            
        tx_data = {
            'from': os.getenv('BLOCKDAG_WALLET_ADDRESS'),
            'to': to_address,
            'value': amount,
            'asset': asset,
            'private_key': private_key
        }
        
        return self.client.send_transaction(tx_data)
    
    def get_transaction_history(self, address: str = None, limit: int = 10) -> List[Dict]:
        """Get transaction history for an address"""
        if not address:
            address = os.getenv('BLOCKDAG_WALLET_ADDRESS')
        return self.client.get_transactions(address, limit=limit)
    
    def generate_wallet(self) -> Dict:
        """Generate a new BlockDAG wallet"""
        return self.client.generate_wallet()
    
    def validate_address(self, address: str) -> bool:
        """Validate a BlockDAG address"""
        return self.client.validate_address(address)
