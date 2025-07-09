from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/market-data')
def market_data():
    # This is a placeholder - in a real app, you'd fetch real market data here
    return jsonify({
        'status': 'success',
        'data': {
            'S&P 500': 4500.50,
            'NASDAQ': 14000.25,
            'DOW': 34500.75
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
