import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from src/config.env
src_dir = Path(__file__).parent.parent / 'src'
load_dotenv(src_dir / 'config.env')

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BLAND_AI_API_KEY = os.getenv('BLAND_AI_API_KEY')
INFURA_API_KEY = os.getenv('INFURA_API_KEY')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

# Wallet Configuration
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')

# Investment Parameters
UNUSED_BALANCE_THRESHOLD = 0.5  # 50% above average monthly spending
MIN_INVESTMENT_AMOUNT = 100  # Minimum amount to consider for investment
MAX_INVESTMENT_AMOUNT = 10000  # Maximum amount for a single investment

# Blockchain Configuration
ETHEREUM_RPC_URL = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
BITCOIN_RPC_URL = os.getenv('BITCOIN_RPC_URL')

# Voice Call Configuration
CALLBACK_URL = os.getenv('CALLBACK_URL')
USER_PHONE_NUMBER = os.getenv('USER_PHONE_NUMBER')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/wallet_monitor.db') 