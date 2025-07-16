# AI Wallet Monitor

An intelligent system that monitors crypto wallet balances, identifies unused funds, and suggests investment opportunities through voice calls.

## Features

- Real-time monitoring of Ethereum and ERC20 token balances
- Analysis of spending patterns to identify unused funds
- Investment suggestions based on market data and technical analysis
- Voice interaction using Bland AI and Gemini AI
- Automated investment execution based on user commands

## Prerequisites

- Python 3.8+
- API keys for:
  - Gemini AI
  - Bland AI
  - Infura (Ethereum)
  - Binance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-wallet-monitor.git
cd ai-wallet-monitor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key
BLAND_AI_API_KEY=your_bland_ai_api_key
INFURA_API_KEY=your_infura_api_key
WALLET_ADDRESS=your_ethereum_wallet_address
PRIVATE_KEY_PATH=path_to_your_encrypted_private_key
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
CALLBACK_URL=your_webhook_url
USER_PHONE_NUMBER=your_phone_number
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. The system will:
   - Monitor your wallet balances daily
   - Identify unused funds based on spending patterns
   - Generate investment suggestions when unused funds are detected
   - Initiate voice calls to discuss investment opportunities
   - Execute investments based on your voice commands

## Project Structure

```
ai_wallet_monitor/
├── config/
│   └── config.py           # Configuration and environment variables
├── src/
│   ├── main.py            # Main application and Flask server
│   ├── wallet_monitor.py  # Wallet balance monitoring
│   ├── investment_analyzer.py  # Investment analysis
│   └── voice_interaction.py    # Voice call handling
├── tests/                 # Test files
├── data/                  # Data storage
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

You can adjust various parameters in `config/config.py`:

- `UNUSED_BALANCE_THRESHOLD`: Percentage above average spending to consider funds as unused
- `MIN_INVESTMENT_AMOUNT`: Minimum amount to consider for investment
- `MAX_INVESTMENT_AMOUNT`: Maximum amount for a single investment
- `ETHEREUM_RPC_URL`: Ethereum node RPC URL
- `BITCOIN_RPC_URL`: Bitcoin node RPC URL

## Security

- Private keys are stored encrypted and never exposed
- API keys are managed through environment variables
- All transactions require voice confirmation
- Investment amounts are capped to prevent large unauthorized transactions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is provided for educational purposes only. Use at your own risk. The developers are not responsible for any financial losses incurred through the use of this software. 