import pandas as pd
from datetime import datetime, timedelta
import logging
from config.config import *
from .mock_wallet import MockWallet

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WalletMonitor:
    def __init__(self):
        # Initialize mock wallet instead of real connections
        self.mock_wallet = MockWallet(initial_balance=10.0)  # Start with 10 ETH
        
    def get_ethereum_balance(self):
        """Get Ethereum balance from mock wallet"""
        return self.mock_wallet.get_ethereum_balance()

    def get_token_balances(self):
        """Get ERC20 token balances from mock wallet"""
        return self.mock_wallet.get_token_balances()

    def get_transaction_history(self, days=30):
        """Get transaction history from mock wallet"""
        return self.mock_wallet.get_transaction_history(days)

    def calculate_spending_patterns(self, days=30):
        """Calculate spending patterns from mock wallet"""
        return self.mock_wallet.calculate_spending_patterns(days)

    def update_balance(self, new_balance):
        """Update the mock wallet balance"""
        self.mock_wallet.update_balance(new_balance)

    def add_transaction(self, amount, is_incoming=True):
        """Add a new transaction to the mock wallet"""
        self.mock_wallet.add_transaction(amount, is_incoming) 