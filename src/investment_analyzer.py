import pandas as pd
import numpy as np
from datetime import datetime
import logging
import ccxt
import requests
from config.config import *
from .wallet_monitor import WalletMonitor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvestmentAnalyzer:
    def __init__(self):
        self.wallet_monitor = WalletMonitor()
        # Initialize Binance exchange without API keys for public data
        self.binance = ccxt.binance({
            'enableRateLimit': True
        })
        self.pol_price = self.get_pol_price()
        
    def get_pol_price(self):
        """Get real-time POL price from CoinGecko"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "matic-network",  # CoinGecko ID for POL (formerly MATIC)
                "vs_currencies": "usd"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data["matic-network"]["usd"]
        except Exception as e:
            logger.error(f"Error fetching POL price: {e}")
            # Fallback to a default price if API fails
            return 0.242130

    def update_pol_price(self):
        """Update POL price"""
        self.pol_price = self.get_pol_price()
        return self.pol_price

    def identify_unused_funds(self):
        """Identify unused funds based on spending patterns and thresholds"""
        try:
            # Get current balance in POL
            current_balance = self.wallet_monitor.get_ethereum_balance()
            
            # Calculate spending patterns in POL
            spending_patterns = self.wallet_monitor.calculate_spending_patterns()
            if not spending_patterns:
                # If no spending patterns, use default threshold (equivalent to ~$50 in POL)
                monthly_average = 206.5  # ~50 USD worth of POL
            else:
                monthly_average = spending_patterns['monthly_average']
            
            # Calculate threshold (50% above monthly spending)
            threshold = monthly_average * (1 + UNUSED_BALANCE_THRESHOLD)
            
            # Calculate unused funds (anything above 3 months of spending)
            safety_net = monthly_average * 3  # Keep 3 months of expenses as safety net
            unused_funds = current_balance - safety_net
            
            if unused_funds >= MIN_INVESTMENT_AMOUNT / self.pol_price:  # Convert USD minimum to POL
                return {
                    'total_balance': current_balance,
                    'monthly_average': monthly_average,
                    'unused_funds': unused_funds,
                    'threshold': threshold,
                    'usd_equivalent': unused_funds * self.pol_price  # Add USD equivalent for reference
                }
            return None
            
        except Exception as e:
            logger.error(f"Error identifying unused funds: {e}")
            return None

    def get_investment_suggestions(self, amount_pol, include_memecoins=False):
        """Get real-time investment suggestions from Binance"""
        try:
            # Update POL price before calculations
            self.update_pol_price()
            
            # Convert POL amount to USD for calculations
            amount_usd = amount_pol * self.pol_price
            
            # Define the trading pairs we want to analyze
            trading_pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
            if include_memecoins:
                trading_pairs.extend(['DOGE/USDT', 'SHIB/USDT', 'PEPE/USDT', 'FLOKI/USDT'])
            
            suggestions = []
            
            for symbol in trading_pairs:
                try:
                    # Get 24h ticker data
                    ticker = self.binance.fetch_ticker(symbol)
                    
                    # Get historical data for risk analysis
                    ohlcv = self.binance.fetch_ohlcv(
                        symbol,
                        timeframe='1d',
                        limit=30
                    )
                    
                    # Convert to DataFrame for analysis
                    df = pd.DataFrame(
                        ohlcv,
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                    )
                    
                    # Calculate daily return
                    daily_return = (ticker['last'] - df['close'].iloc[-1]) / df['close'].iloc[-1]
                    
                    # Calculate volatility
                    volatility = (df['high'] - df['low']).mean() / df['close'].mean()
                    
                    # Determine risk level based on volatility and if it's a memecoin
                    is_memecoin = symbol in ['DOGE/USDT', 'SHIB/USDT', 'PEPE/USDT', 'FLOKI/USDT']
                    if is_memecoin:
                        risk_level = 'extreme'
                        risk_warning = "⚠️ High volatility asset with significant risk of loss. Only invest what you can afford to lose."
                    else:
                        if volatility < 0.02:
                            risk_level = 'low'
                            risk_warning = None
                        elif volatility < 0.05:
                            risk_level = 'medium'
                            risk_warning = None
                        else:
                            risk_level = 'high'
                            risk_warning = None
                    
                    suggestion = {
                        'symbol': symbol,
                        'price': ticker['last'],
                        'price_in_pol': ticker['last'] / self.pol_price,  # Add price in POL
                        'risk_level': risk_level,
                        'daily_return': daily_return,
                        'volume': ticker['quoteVolume'],
                        'volume_in_pol': ticker['quoteVolume'] / self.pol_price,  # Add volume in POL
                        'is_memecoin': is_memecoin,
                        'risk_warning': risk_warning
                    }
                    
                    suggestions.append(suggestion)
                    
                except Exception as e:
                    logger.error(f"Error fetching data for {symbol}: {e}")
                    continue
            
            # Sort suggestions: First by type (standard then memecoins), then by daily return
            suggestions.sort(key=lambda x: (x['is_memecoin'], -x['daily_return']))
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting investment suggestions: {e}")
            return []

    def get_matic_price(self):
        """Get current MATIC price in USD"""
        try:
            ticker = self.binance.fetch_ticker('MATIC/USDT')
            return ticker['last']
        except Exception as e:
            logger.error(f"Error fetching MATIC price: {e}")
            return None

    def _get_risk_level(self, risk_score):
        """Convert risk score to risk level"""
        if risk_score < 0.1:
            return 'low'
        elif risk_score < 0.3:
            return 'medium'
        else:
            return 'high'

    def analyze_investment_opportunity(self, symbol, amount):
        """Analyze a specific investment opportunity"""
        try:
            # Get historical data
            ohlcv = self.binance.fetch_ohlcv(
                symbol,
                timeframe='1d',
                limit=30
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Calculate technical indicators
            df['sma_7'] = df['close'].rolling(window=7).mean()
            df['sma_30'] = df['close'].rolling(window=30).mean()
            df['rsi'] = self._calculate_rsi(df['close'])
            
            # Get current price
            current_price = self.binance.fetch_ticker(symbol)['last']
            
            # Generate analysis
            analysis = {
                'current_price': current_price,
                'trend': 'bullish' if df['sma_7'].iloc[-1] > df['sma_30'].iloc[-1] else 'bearish',
                'rsi': df['rsi'].iloc[-1],
                'volatility': (df['high'] - df['low']).mean() / df['close'].mean(),
                'volume_trend': 'increasing' if df['volume'].iloc[-1] > df['volume'].mean() else 'decreasing'
            }
            
            # Add risk assessment
            analysis['risk_level'] = self._assess_risk(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing investment opportunity: {e}")
            return None

    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def _assess_risk(self, analysis):
        """Assess risk level based on technical analysis"""
        risk_score = 0
        
        # Trend analysis
        risk_score += 1 if analysis['trend'] == 'bullish' else 2
        
        # RSI analysis
        if analysis['rsi'] > 70:
            risk_score += 2
        elif analysis['rsi'] < 30:
            risk_score += 0
        else:
            risk_score += 1
            
        # Volatility analysis
        if analysis['volatility'] > 0.05:
            risk_score += 2
        else:
            risk_score += 1
            
        # Volume analysis
        risk_score += 1 if analysis['volume_trend'] == 'increasing' else 2
        
        # Convert to risk level
        if risk_score <= 3:
            return 'low'
        elif risk_score <= 5:
            return 'medium'
        else:
            return 'high' 