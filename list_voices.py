import requests

# API Key from the previous successful test
api_key = "org_64881a7d5f7ba2fa7b7725243f402f38a9b409ea523fdcc97ca89ff1dccf233c1d8b05cf7a46cf64fe2469"

def list_available_voices():
    """List all available voices"""
    url = "https://api.bland.ai/v1/voices"
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        print("Fetching available voices...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print("Response Body:")
        
        if response.status_code == 200:
            voices = response.json()
            print(json.dumps(voices, indent=2))
            
            if isinstance(voices, list) and len(voices) > 0:
                print("\nAvailable Voices:")
                for i, voice in enumerate(voices, 1):
                    print(f"{i}. {voice.get('name')} ({voice.get('voice_id')})")
            return True
        else:
            print(response.text)
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    import json
    list_available_voices()
