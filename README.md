# Oscar AI - Financial Assistant

A smart financial assistant that provides real-time market updates and investment advice through voice calls.

## Features

- 📞 Voice-based financial assistance
- 📊 Real-time market data
- 📈 Stock market analysis
- 💰 Investment recommendations
- 🔒 Secure transaction handling

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/chhaavii/OSCARR.git
   cd OSCARR
   ```

2. **Set up environment variables**
   Create a `.env` file with your API keys:
   ```
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   BLAND_AI_API_KEY=your_bland_ai_key
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the web interface**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000` in your browser.

2. **Make a call**
   - Enter a phone number with country code
   - Select a call type (Market Update, Portfolio Review, etc.)
   - Click "Call Me"

## Technologies Used

- Python
- Flask
- Alpha Vantage API
- Bland AI API
- Tailwind CSS
- GitHub Pages

## License

MIT

---

*Note: Replace the placeholder API keys with your actual keys before deployment.*
