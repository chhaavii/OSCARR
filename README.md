# OSCARR - AI Investment Assistant

> **O**perational **S**mart **C**ontract **A**utomated **R**eporting **R**obo-advisor

An intelligent AI-powered investment assistant that monitors your crypto portfolio, identifies investment opportunities, and executes trades through voice commands.

## ✨ Key Features

- **Voice-First Interface**
  - Natural language processing with Gemini AI
  - Voice calls for investment discussions
  - Secure voice confirmation for transactions

- **Blockchain Integration**
  - Real-time portfolio monitoring across multiple chains
  - BlockDAG Network integration for fast, low-cost transactions
  - Smart contract-based investment strategies

- **Intelligent Investing**
  - AI-driven market analysis
  - Personalized investment recommendations
  - Risk assessment and portfolio balancing

- **Security**
  - End-to-end encrypted communications
  - Multi-factor authentication
  - Non-custodial asset management

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+ (for frontend)
- API Keys:
  - Gemini AI
  - Bland AI
  - BlockDAG Network
  - Infura (Ethereum)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/chhaavii/OSCARR.git
cd OSCARR
```

2. Set up the environment:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

3. Configure environment variables:
Create a `.env` file in the root directory:
```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key
BLAND_AI_API_KEY=your_bland_ai_api_key
BLOCKDAG_API_KEY=your_blockdag_api_key
INFURA_API_KEY=your_infura_api_key

# Wallet Configuration
WALLET_ADDRESS=your_eth_address
PRIVATE_KEY=your_encrypted_private_key

# BlockDAG Network
BLOCKDAG_NETWORK=testnet  # or mainnet
BLOCKDAG_WALLET=your_blockdag_wallet

# Call Configuration
CALLBACK_URL=https://your-webhook-url.com
DEFAULT_PHONE=+1234567890  # Your verified phone number

# Security
CONFIRMATION_WORD=rates
ENCRYPTION_KEY=your_encryption_key
```

## 🚦 Usage

### Starting the Application

1. **Backend Server**:
```bash
# Start the backend server
python src/main.py
```

2. **Frontend Development**:
```bash
cd frontend
npm run dev
```

### Making Your First Investment Call

1. OSCARR will monitor your wallet 24/7
2. When investment opportunities are found, you'll receive a call
3. Discuss options with the AI assistant
4. Confirm transactions by saying the confirmation word: "rates"

### Voice Commands

- "What's my portfolio balance?"
- "Show me investment opportunities"
- "Invest 100 USD in ETH"
- "Sell 50% of my BTC"
- "What's the market sentiment?"

## 🏗️ Project Structure

```
OSCARR/
├── src/
│   ├── config/                  # Configuration files
│   │   ├── config.py            # Main configuration
│   │   └── blockdag_config.py   # BlockDAG settings
│   │
│   ├── core/                   # Core functionality
│   │   ├── main.py             # Application entry point
│   │   ├── wallet_monitor.py   # Portfolio monitoring
│   │   └── investment_analyzer.py  # Market analysis
│   │
│   ├── blockchain/            # Blockchain integrations
│   │   ├── blockdag_wallet.py  # BlockDAG wallet
│   │   └── ethereum.py        # Ethereum interactions
│   │
│   └── ai/                    # AI components
│       ├── voice_interaction.py  # Voice processing
│       └── nlp_processor.py   # Natural language understanding
│
├── frontend/                 # Web interface
│   ├── public/
│   └── src/
│
├── tests/                   # Test suite
├── data/                   # Local data storage
├── scripts/               # Utility scripts
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## ⚙️ Configuration

### Key Parameters

Edit `src/config/config.py` to customize:

```python
# Investment Parameters
INVESTMENT = {
    'min_amount': 10.0,        # Minimum investment amount in USD
    'max_amount': 10000.0,     # Maximum single investment
    'slippage': 0.5,          # Max allowed slippage %
    'risk_profile': 'moderate' # Risk tolerance (low/moderate/high)
}

# BlockDAG Settings
BLOCKDAG = {
    'confirmations': 6,        # Required confirmations
    'gas_limit': 21000,        # Default gas limit
    'max_fee': 100             # Max fee in Gwei
}

# Voice Settings
VOICE = {
    'confirmation_word': 'rates',
    'language': 'en-US',
    'speech_rate': 1.0
}
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ |
| `BLAND_AI_API_KEY` | Bland AI voice API key | ✅ |
| `BLOCKDAG_API_KEY` | BlockDAG Network API key | ✅ |
| `INFURA_API_KEY` | Infura API key | ✅ |
| `WALLET_ADDRESS` | Your Ethereum address | ✅ |
| `PRIVATE_KEY` | Encrypted private key | ✅ |
| `CONFIRMATION_WORD` | Word for transaction confirmation | ✅ |
| `ENCRYPTION_KEY` | For sensitive data encryption | ✅ |

## 🔒 Security

### Data Protection

- Private keys are encrypted at rest
- API keys never leave the server
- All communications are end-to-end encrypted
- Regular security audits

### Transaction Security

- Multi-signature wallet support
- Transaction simulation before execution
- Rate limiting and anti-fraud measures
- Automatic transaction monitoring

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [BlockDAG Network](https://blockdag.network/) for the high-performance blockchain infrastructure
- [Google Gemini](https://gemini.google.com/) for AI capabilities
- [Bland AI](https://bland.ai/) for voice technology

---

<div align="center">
  Made with ❤️ by the OSCARR Team
</div>

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