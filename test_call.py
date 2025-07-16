import requests
import json

def make_test_call(phone_number):
    """Make a test call using Bland AI API"""
    url = "https://api.bland.ai/v1/calls"
    
    # API Key from the previous successful test
    api_key = "org_64881a7d5f7ba2fa7b7725243f402f38a9b409ea523fdcc97ca89ff1dccf233c1d8b05cf7a46cf64fe2469"
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "phone_number": phone_number,
        "task": "This is a test call from OSCARR. Please let us know if you receive this call.",
        "model": "enhanced"
        # Let the API use the default voice for the account
    }

    print(f"Initiating test call to {phone_number}...")
    print(f"Using API Key: {api_key[:10]}...{api_key[-10:]}")
    print("Request payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            json=payload,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print("Response Headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
            
        print("\nResponse Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
            
        response.raise_for_status()
        
        result = response.json()
        if result.get('status') == 'success':
            print(f"\n✅ Call initiated successfully!")
            print(f"Call ID: {result.get('call_id')}")
            return True
        else:
            print("\n❌ Failed to initiate call:")
            print(json.dumps(result, indent=2))
            return False
            
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP Error: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {str(e)}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    
    return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python test_call.py +1234567890")
        print("Please include the phone number with country code")
        sys.exit(1)
        
    make_test_call(sys.argv[1])
