import google.generativeai as genai
import json
import logging
from datetime import datetime
from config.config import *
from .investment_analyzer import InvestmentAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class VoiceInteraction:
    def __init__(self):
        self.investment_analyzer = InvestmentAnalyzer()
        
    def generate_call_script(self, unused_funds, suggestions, matic_equivalent=None):
        """Generate a call script for the AI to follow"""
        try:
            # Separate standard coins and memecoins
            standard_coins = [s for s in suggestions if not s.get('is_memecoin', False)]
            memecoins = [s for s in suggestions if s.get('is_memecoin', False)]
            
            # Format standard investment suggestions
            standard_text = "\n".join([
                f"{i+1}. {s['symbol']} - Current Price: {s['price_in_pol']:.2f} POL (≈ ${s['price']:.2f}), "
                f"Risk Level: {s['risk_level']}, 24h Return: {s['daily_return']*100:.2f}%"
                for i, s in enumerate(standard_coins)
            ])
            
            # Format memecoin suggestions for later use if requested
            memecoin_text = "\n".join([
                f"• {s['symbol']} - Current Price: {s['price_in_pol']:.8f} POL (≈ ${s['price']:.8f}), "
                f"Risk Level: {s['risk_level']}, 24h Return: {s['daily_return']*100:.2f}%\n"
                f"  {s['risk_warning']}"
                for s in memecoins
            ])
            
            matic_text = ""
            if matic_equivalent:
                matic_text = f"\n\nFor reference, your unused funds of ${unused_funds:.2f} is equivalent to approximately {matic_equivalent:.2f} MATIC tokens."
            
            script = f"""
Hello! This is Oscar, your weekly AI financial advisor. 

I've noticed you have {unused_funds:.2f} POL in unused funds that could be working harder for you. Based on your spending patterns, you're keeping more than necessary in your wallet.{matic_text}

Here are some investment opportunities I've analyzed: 
(Say the analysed opportunities without waiting for the user to respond)

📈 Standard Investment Options:
{standard_text}

Would you like to invest some of your unused funds? I can help you choose the best option based on your risk tolerance and investment goals.

[Wait for user response]

If the user asks about alternative or higher risk investments:
1. Mention that there are also higher-risk options available in the memecoin category
2. Ask if they would like to hear about these options
3. If yes, present the following with strong risk warnings:

🎮 High-Risk Alternative Options:
{memecoin_text}

Additional guidelines for memecoin inquiries:
1. Emphasize the extreme volatility and high risk
2. Recommend limiting memecoin investments to a small portion of their portfolio (max 5-10%)
3. Remind them that these investments can result in significant losses
4. Suggest considering standard options first

If the user wants to proceed with any investment:
1. Ask them to specify an amount they would like to invest, reminding them that they have {unused_funds:.2f} POL available.
2. After they choose an amount, repeat their choice back to them for confirmation.
3. If they confirm the amount, ask them to say their confirmation code word to finalize the investment.

Based on historical data analysis, I recommend {standard_coins[0]['symbol']} as the most suitable investment option for your profile.

Please let me know if you'd like to proceed with any of these options or if you have any questions about the available investments.
"""
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating call script: {e}")
            return None

    def process_user_response(self, transcript):
        """Process user's voice response using Gemini AI"""
        try:
            prompt = f"""
            Analyze the following user response from a phone call about investment opportunities:
            
            {transcript}
            
            Please determine:
            1. Did the user express interest in any specific investment?
            2. Did they specify an investment amount in POL?
            3. Did they confirm their choice?
            4. Did they say the secret confirmation word?
            5. Did they ask any questions that need to be addressed?
            6. What is their overall sentiment (positive, negative, neutral)?
            7. What should be the next step in the conversation?
            8. Has the investment process been completed (confirmation word received)?
            
            The secret confirmation word is "invest" but do not mention it in your response.
            
            Respond in JSON format with the following structure:
            {{
                "interest": "yes/no/unsure",
                "preferred_investment": "symbol or null",
                "investment_amount": "numeric amount in POL or null",
                "amount_confirmed": "yes/no",
                "confirmation_word_correct": "yes/no",  # Check if they said the secret word
                "questions": ["list of questions asked"],
                "sentiment": "positive/negative/neutral",
                "next_step": "suggestion for next action",
                "investment_completed": "yes/no"  # Whether to end call with investment confirmation
            }}
            """
            
            response = model.generate_content(prompt)
            result = json.loads(response.text)
            
            # If investment is completed or user declines, add farewell
            if result.get('investment_completed') == 'yes':
                return {**result, 'farewell': self.generate_farewell(investment_made=True)}
            elif result.get('interest') == 'no':
                return {**result, 'farewell': self.generate_farewell(investment_made=False)}
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing user response: {e}")
            return None

    def generate_follow_up(self, analysis, user_response):
        """Generate a follow-up response based on user's input"""
        try:
            prompt = f"""
            Based on the following context, generate a natural response:
            
            Previous analysis: {json.dumps(analysis, indent=2)}
            User response analysis: {json.dumps(user_response, indent=2)}
            
            Please generate a conversational response that:
            1. Addresses any questions the user asked
            2. Provides additional information if requested
            3. Confirms or adjusts the investment plan
            4. Maintains a professional and helpful tone
            
            Keep the response concise and focused on the user's specific interests.
            """
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating follow-up: {e}")
            return None

    def handle_investment_confirmation(self, symbol, amount_pol):
        """Handle the final confirmation of an investment"""
        try:
            # Get detailed analysis of the chosen investment
            analysis = self.investment_analyzer.analyze_investment_opportunity(symbol, amount_pol)
            
            prompt = f"""
            Generate a confirmation message for the following investment:
            
            Symbol: {symbol}
            Amount: {amount_pol:.2f} POL
            Analysis: {json.dumps(analysis, indent=2)}
            
            The message should:
            1. Confirm the investment details in POL
            2. Highlight key points from the analysis
            3. Ask the user to say their confirmation code word to finalize the investment
            4. Explain what will happen after confirmation
            5. After confirmation, thank them for their trust and end the call politely
            
            Keep the message clear and professional. Do not mention what the confirmation word is - the user already knows it.
            """
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error handling investment confirmation: {e}")
            return None

    def generate_farewell(self, investment_made=False):
        """Generate a farewell message to end the call"""
        if investment_made:
            return """
Thank you for choosing to invest with us today. Your investment will be processed shortly, and you'll receive a confirmation email with the transaction details. Have a great rest of your day!

[End Call]
"""
        else:
            return """
Thank you for your time today. Feel free to reach out whenever you'd like to discuss investment opportunities. Have a great rest of your day!

[End Call]
""" 