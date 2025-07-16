from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from datetime import datetime
import os
import requests
from config.config import *
from src.wallet_monitor import WalletMonitor
from src.investment_analyzer import InvestmentAnalyzer
from src.voice_interaction import VoiceInteraction

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
scheduler = BackgroundScheduler()

# Initialize components
wallet_monitor = WalletMonitor()
investment_analyzer = InvestmentAnalyzer()
voice_interaction = VoiceInteraction()

def make_bland_ai_call(script):
    """Make a call using Bland AI"""
    try:
        url = "https://api.bland.ai/v1/calls"
        
        headers = {
            "Authorization": f"Bearer {BLAND_AI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "phone_number": USER_PHONE_NUMBER,
            "task": script,
            "webhook_url": CALLBACK_URL,
            "model": "enhanced"  # Use enhanced model for better voice quality
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        call_id = response.json().get('call_id')
        logger.info(f"Call initiated successfully. Call ID: {call_id}")
        return call_id
        
    except Exception as e:
        logger.error(f"Error making Bland AI call: {e}")
        return None

def check_unused_funds():
    """Periodically check for unused funds and initiate calls if needed"""
    try:
        # Identify unused funds
        unused_funds_data = investment_analyzer.identify_unused_funds()
        if not unused_funds_data:
            return
            
        unused_funds = unused_funds_data['unused_funds']
        logger.info(f"Found unused funds: ${unused_funds:.2f}")
        
        # Get investment suggestions
        suggestions = investment_analyzer.get_investment_suggestions(unused_funds)
        if not suggestions:
            logger.warning("No investment suggestions available")
            return
            
        # Generate call script
        script = voice_interaction.generate_call_script(unused_funds, suggestions)
        if not script:
            logger.error("Failed to generate call script")
            return
            
        # Make the actual call using Bland AI
        call_id = make_bland_ai_call(script)
        if call_id:
            logger.info(f"Call initiated successfully. Call ID: {call_id}")
        else:
            logger.error("Failed to initiate call")
        
    except Exception as e:
        logger.error(f"Error in check_unused_funds: {e}")

@app.route('/webhook/bland-ai', methods=['POST'])
def handle_bland_ai_webhook():
    """Handle webhooks from Bland AI"""
    try:
        data = request.json
        transcript = data.get('transcript', '')
        call_status = data.get('status', '')
        
        if call_status == 'completed':
            # Process user's response
            user_response = voice_interaction.process_user_response(transcript)
            if not user_response:
                return jsonify({'status': 'error', 'message': 'Failed to process user response'})
                
            # Handle investment confirmation if user expressed interest
            if user_response['interest'] == 'yes' and user_response['preferred_investment']:
                symbol = user_response['preferred_investment']
                amount = min(unused_funds, MAX_INVESTMENT_AMOUNT)
                
                confirmation = voice_interaction.handle_investment_confirmation(symbol, amount)
                if confirmation:
                    # Make follow-up call with confirmation
                    make_bland_ai_call(confirmation)
                    logger.info(f"Investment confirmation call made")
                    
            # Generate follow-up if needed
            elif user_response['questions'] or user_response['next_step'] != 'end':
                follow_up = voice_interaction.generate_follow_up(
                    investment_analyzer.analyze_investment_opportunity(symbol, amount),
                    user_response
                )
                if follow_up:
                    # Make follow-up call
                    make_bland_ai_call(follow_up)
                    logger.info(f"Follow-up call made")
                    
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Error handling Bland AI webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

def start_scheduler():
    """Start the background scheduler"""
    scheduler.add_job(
        check_unused_funds,
        'interval',
        hours=24,  # Check daily
        next_run_time=datetime.now()
    )
    scheduler.start()

if __name__ == '__main__':
    # Start the scheduler
    start_scheduler()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001) 