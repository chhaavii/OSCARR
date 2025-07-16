import os
import json
import requests
from dotenv import load_dotenv

def make_call(phone_number):
    """
    Make a call using Bland AI API
    """
    load_dotenv('src/config.env')
    
    api_key = os.getenv('BLAND_AI_API_KEY')
    if not api_key:
        print("Error: BLAND_AI_API_KEY not found in config.env")
        return

    url = "https://api.bland.ai/v1/calls"
    
    headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "phone_number": phone_number,
        "task": """Hello, this is Oscar, your personal investment advisor. I'm calling because I've identified some excellent investment opportunities that align with your financial goals. 
        
        As your personal advisor, I can help you with:
        - Analyzing market trends
        - Making investment decisions
        - Executing transactions on your behalf
        - Managing your portfolio
        
        I noticed you have some funds that could be working harder for you. Would you like me to walk you through some personalized investment options?
        
        (Note: Please say 'invest' at any time to authorize a transaction, or 'stop' to end this call)""",
        "webhook_url": "https://webhook.site/ddd50ba8-fe27-40f5-baf4-faa0737b11ba",
        "model": "enhanced",
        "first_sentence": "Hello, this is Oscar, your personal investment advisor. Is this a good time to talk?",
        "record": True,
        "temperature": 0.7
    }

    try:
        print(f"Initiating call to {phone_number}...")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if result.get('status') == 'success':
            print(f"✅ Call initiated successfully!")
            print(f"Call ID: {result.get('call_id')}")
            print(f"Status: {result.get('message')}")
        else:
            print("❌ Failed to initiate call:")
            print(json.dumps(result, indent=2))
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making the request: {str(e)}")
    except json.JSONDecodeError:
        print("❌ Error parsing API response")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python make_call.py +1234567890")
        print("Please include the phone number with country code")
        sys.exit(1)
        
    phone_number = sys.argv[1]
    make_call(phone_number)
