import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from config.config import *

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockWallet:
    def __init__(self, initial_balance=1000.0):
        self.initial_balance = initial_balance  # Store initial balance
        self.balance = initial_balance  # Current balance in USD
        self.transactions = []
        self._last_reset_time = datetime.now()  # Initialize last reset time
        self._generate_initial_transactions()

    def _generate_initial_transactions(self):
        """Generate initial transaction history for the mock wallet"""
        start_date = datetime.now() - timedelta(days=30)
        for i in range(30):
            date = start_date + timedelta(days=i)
            # Simulate daily transactions
            daily_transactions = np.random.randint(1, 3)
            for _ in range(daily_transactions):
                amount = np.random.uniform(5.0, 50.0)  # USD amounts
                is_incoming = np.random.choice([True, False])
                self.transactions.append({
                    'hash': f'mock_tx_{i}_{_}',
                    'from': 'sender_address' if is_incoming else 'mock_address',
                    'to': 'mock_address' if is_incoming else 'recipient_address',
                    'value': amount,
                    'timestamp': date,
                    'is_incoming': is_incoming
                })

    def get_ethereum_balance(self):
        """Get mock balance in USD"""
        # Calculate current balance based on initial balance and recent transactions
        current_balance = self.initial_balance
        
        # Only consider transactions from the last reset
        recent_transactions = [tx for tx in self.transactions if tx['timestamp'] > self._last_reset_time]
        
        for tx in recent_transactions:
            if tx['is_incoming']:
                current_balance += tx['value']
            else:
                current_balance -= tx['value']
        
        self.balance = current_balance
        logger.info(f"Mock balance: ${self.balance:.2f}")
        return self.balance

    def get_token_balances(self):
        """Get mock token balances in USD"""
        return {
            'USDT': self.balance * 0.5,
            'USDC': self.balance * 0.3
        }

    def get_transaction_history(self, days=30):
        """Get mock transaction history"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        filtered_transactions = [
            tx for tx in self.transactions
            if start_date <= tx['timestamp'] <= end_date
        ]
        
        return pd.DataFrame(filtered_transactions)

    def calculate_spending_patterns(self, days=30):
        """Calculate mock spending patterns"""
        transactions = self.get_transaction_history(days)
        if transactions.empty:
            return None
        
        # Only consider outgoing transactions for spending patterns
        spending_transactions = transactions[~transactions['is_incoming']]
        
        daily_spending = spending_transactions.groupby(
            spending_transactions['timestamp'].dt.date
        )['value'].sum()
        
        weekly_spending = spending_transactions.groupby(
            spending_transactions['timestamp'].dt.isocalendar().week
        )['value'].sum()
        
        return {
            'daily_average': daily_spending.mean() if not daily_spending.empty else 50.0,
            'weekly_average': weekly_spending.mean() if not weekly_spending.empty else 350.0,
            'monthly_average': (daily_spending.mean() * 30) if not daily_spending.empty else 1500.0
        }

    def update_balance(self, new_balance):
        """Update the mock wallet balance"""
        self.balance = new_balance
        self.initial_balance = new_balance  # Update initial balance too
        # Clear previous transactions and regenerate history
        self.transactions = []
        self._last_reset_time = datetime.now()  # Track when we last reset
        self._generate_initial_transactions()
        logger.info(f"Updated mock wallet balance to: ${self.balance:.2f}")

    def add_transaction(self, amount, is_incoming=True):
        """Add a new mock transaction"""
        transaction = {
            'hash': f'mock_tx_{len(self.transactions)}',
            'from': 'sender_address' if is_incoming else 'mock_address',
            'to': 'mock_address' if is_incoming else 'recipient_address',
            'value': amount,
            'timestamp': datetime.now(),
            'is_incoming': is_incoming
        }
        self.transactions.append(transaction)
        
        if is_incoming:
            self.balance += amount
        else:
            self.balance -= amount
            
        logger.info(f"Added mock transaction: ${amount:.2f} (incoming: {is_incoming})")
        logger.info(f"New balance: ${self.balance:.2f}") 