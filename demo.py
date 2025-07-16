import time
from src.wallet_monitor import WalletMonitor
from src.investment_analyzer import InvestmentAnalyzer
from src.voice_interaction import VoiceInteraction
from src.conversation_logger import ConversationLogger
import requests
import logging
from config.config import *
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_bland_ai_call(script):
    """Make a call using Bland AI"""
    try:
        url = "https://api.bland.ai/v1/calls"
        
        headers = {
            "Authorization": f"Bearer {BLAND_AI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Get phone number and webhook URL from environment variables
        phone_number = os.getenv('USER_PHONE_NUMBER')
        webhook_url = os.getenv('CALLBACK_URL')
        
        data = {
            "phone_number": phone_number,
            "task": script,
            "webhook_url": webhook_url,
            "model": "enhanced"  # Use enhanced model for better voice quality
        }
        
        logger.info(f"Making call to {phone_number}")
        logger.info(f"Using webhook URL: {webhook_url}")
        logger.info(f"Using API key: {BLAND_AI_API_KEY[:10]}...")
        
        response = requests.post(url, headers=headers, json=data)
        
        logger.info(f"API Response Status: {response.status_code}")
        logger.info(f"API Response Headers: {response.headers}")
        logger.info(f"API Response Body: {response.text}")
        
        response.raise_for_status()
        
        call_data = response.json()
        logger.info(f"Call initiated successfully. Response: {call_data}")
        return call_data.get('call_id')
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error making Bland AI call: {e}")
        logger.error(f"Response text: {e.response.text if hasattr(e, 'response') else 'No response text'}")
        return None
    except Exception as e:
        logger.error(f"Error making Bland AI call: {e}")
        return None

def run_demo():
    print("🚀 Starting AI Wallet Monitor Demo")
    print("----------------------------------")
    
    # Initialize components
    wallet_monitor = WalletMonitor()
    investment_analyzer = InvestmentAnalyzer()
    voice_interaction = VoiceInteraction()
    conversation_logger = ConversationLogger()
    
    # Get current POL price
    pol_price = investment_analyzer.get_pol_price()
    
    # Set up high balance scenario
    print("\n📊 Scenario: High Balance with Unused Funds")
    print("Description: Showing unused funds detection and investment opportunities")
    print("----------------------------------")
    
    # Set initial balance to 4132 POL (approximately $1000 worth)
    initial_pol = 4132  # $1000 / $0.242 = 4132 POL
    wallet_monitor.update_balance(initial_pol)
    print(f"Initial Balance: {initial_pol:.2f} POL (≈ ${initial_pol * pol_price:.2f})")
    
    # Log initial state
    conversation_logger.log_initial_state(initial_pol, pol_price, 207)  # 207 POL monthly spending
    
    # Add some transactions to show normal usage
    print("\n💸 Recent Transaction History:")
    # Convert USD amounts to POL
    pol_spent_groceries = 83  # $20 / $0.242
    pol_spent_transport = 62  # $15 / $0.242
    pol_received_salary = 6198  # $1500 / $0.242
    
    wallet_monitor.add_transaction(pol_spent_groceries, is_incoming=False)
    transaction_msg = f"Spent {pol_spent_groceries:.2f} POL (≈ ${pol_spent_groceries * pol_price:.2f}) on groceries"
    print(f"- {transaction_msg}")
    conversation_logger.log_interaction("system", transaction_msg, {"type": "transaction", "amount_pol": pol_spent_groceries})
    
    wallet_monitor.add_transaction(pol_spent_transport, is_incoming=False)
    transaction_msg = f"Spent {pol_spent_transport:.2f} POL (≈ ${pol_spent_transport * pol_price:.2f}) on transportation"
    print(f"- {transaction_msg}")
    conversation_logger.log_interaction("system", transaction_msg, {"type": "transaction", "amount_pol": pol_spent_transport})
    
    wallet_monitor.add_transaction(pol_received_salary, is_incoming=True)
    transaction_msg = f"Received {pol_received_salary:.2f} POL (≈ ${pol_received_salary * pol_price:.2f}) from salary"
    print(f"- {transaction_msg}")
    conversation_logger.log_interaction("system", transaction_msg, {"type": "transaction", "amount_pol": pol_received_salary})
    
    # Show current balance
    current_balance = wallet_monitor.get_ethereum_balance()
    balance_msg = f"Current Balance: {current_balance:.2f} POL (≈ ${current_balance * pol_price:.2f})"
    print(f"\n💰 {balance_msg}")
    conversation_logger.log_interaction("system", balance_msg, {"type": "balance_update", "balance_pol": current_balance})
    
    # Calculate monthly spending (around 207 POL ≈ $50)
    monthly_spending_pol = 207
    safety_net = monthly_spending_pol * 3  # Keep 3 months of expenses as safety net
    unused_funds = current_balance - safety_net
    
    if unused_funds >= 100:  # Minimum investment amount in POL
        unused_funds_msg = (
            f"Unused Funds Detected!\n"
            f"Monthly Spending: {monthly_spending_pol:.2f} POL (≈ ${monthly_spending_pol * pol_price:.2f})\n"
            f"Safety Net (3 months): {safety_net:.2f} POL (≈ ${safety_net * pol_price:.2f})\n"
            f"Unused Funds Available: {unused_funds:.2f} POL (≈ ${unused_funds * pol_price:.2f})"
        )
        print(f"\n💡 {unused_funds_msg}")
        conversation_logger.log_interaction("system", unused_funds_msg, {
            "type": "unused_funds_detection",
            "monthly_spending_pol": monthly_spending_pol,
            "safety_net_pol": safety_net,
            "unused_funds_pol": unused_funds
        })
        
        # Get investment suggestions
        print("\n🔍 Analyzing Investment Opportunities...")
        suggestions = investment_analyzer.get_investment_suggestions(unused_funds, include_memecoins=True)
        
        if suggestions:
            print("\n📈 Real-Time Investment Opportunities:")
            conversation_logger.log_investment_suggestions(suggestions)
            
            # Print standard investments
            standard_coins = [s for s in suggestions if not s.get('is_memecoin', False)]
            print("\n📊 Standard Investment Options:")
            for i, suggestion in enumerate(standard_coins, 1):
                print(f"\n{i}. {suggestion['symbol']}")
                print(f"   Current Price: {suggestion['price_in_pol']:.2f} POL (${suggestion['price']:.2f})")
                print(f"   Risk Level: {suggestion['risk_level']}")
                print(f"   24h Return: {suggestion['daily_return']*100:.2f}%")
                print(f"   24h Volume: {suggestion['volume_in_pol']:,.2f} POL (${suggestion['volume']:,.2f})")
            
            # Print memecoin investments if any
            memecoins = [s for s in suggestions if s.get('is_memecoin', False)]
            if memecoins:
                print("\n🎮 Memecoin Options (Extremely High Risk):")
                for i, suggestion in enumerate(memecoins, len(standard_coins) + 1):
                    print(f"\n{i}. {suggestion['symbol']}")
                    print(f"   Current Price: {suggestion['price_in_pol']:.8f} POL (${suggestion['price']:.8f})")
                    print(f"   Risk Level: {suggestion['risk_level']}")
                    print(f"   24h Return: {suggestion['daily_return']*100:.2f}%")
                    print(f"   24h Volume: {suggestion['volume_in_pol']:,.2f} POL (${suggestion['volume']:,.2f})")
                    if suggestion['risk_warning']:
                        print(f"   {suggestion['risk_warning']}")
            
            # Generate call script
            script = voice_interaction.generate_call_script(unused_funds, suggestions)
            
            if script:
                print("\n🗣️ AI Call Script:")
                print("----------------------")
                print(script)
                conversation_logger.log_interaction("ai", script, {"type": "call_script"})
                
                # Make the actual call using Bland AI
                print("\n📞 Initiating Phone Call...")
                call_id = make_bland_ai_call(script)
                if call_id:
                    call_msg = (
                        f"Call initiated successfully! Call ID: {call_id}\n"
                        f"You should receive a call at {os.getenv('USER_PHONE_NUMBER')}\n"
                        f"Webhook URL for responses: {os.getenv('CALLBACK_URL')}"
                    )
                    print(f"✅ {call_msg}")
                    conversation_logger.log_interaction("system", call_msg, {
                        "type": "call_initiated",
                        "call_id": call_id
                    })
                else:
                    error_msg = "Failed to initiate call. Check the logs for details."
                    print(f"❌ {error_msg}")
                    conversation_logger.log_interaction("system", error_msg, {"type": "call_error"})
                
                print("\n⏳ Waiting for your response on the phone...")
                print("The system will process your voice response and make investment decisions accordingly.")
                
                # Simulate a successful investment response
                print("\n🔄 Simulating user response and investment process...")
                time.sleep(2)
                
                # Convert investment amount to POL
                investment_amount_pol = 2066  # $500 worth of POL
                
                # Simulate a successful investment response
                response = {
                    'interest': 'yes',
                    'preferred_investment': 'BTC/USDT',
                    'investment_amount': investment_amount_pol,
                    'amount_confirmed': 'yes',
                    'confirmation_word_correct': 'yes',
                    'questions': [],
                    'sentiment': 'positive',
                    'next_step': 'finalize investment',
                    'investment_completed': 'yes',
                    'farewell': voice_interaction.generate_farewell(investment_made=True)
                }
                
                # Log user's decision
                conversation_logger.log_interaction("user", "Confirmed investment decision", response)
                
                print("\n📱 Call Summary:")
                summary_msg = f"User chose to invest {response['investment_amount']:.2f} POL (≈ ${response['investment_amount'] * pol_price:.2f}) in {response['preferred_investment']}"
                print(f"- {summary_msg}")
                print("- Investment confirmed with security code word")
                
                # Log final investment decision
                conversation_logger.log_investment_decision(response)
                
                print("\n🗣️ Ending Call:")
                print(response['farewell'])
                conversation_logger.log_interaction("ai", response['farewell'], {"type": "farewell"})
                
                # Save conversation summary
                summary_file = conversation_logger.save_summary()
                print(f"\n📝 Conversation summary saved to: {summary_file}")
                
    else:
        msg = "No unused funds detected at this time"
        print(f"\nℹ️ {msg}")
        conversation_logger.log_interaction("system", msg, {"type": "no_unused_funds"})

if __name__ == "__main__":
    run_demo() 