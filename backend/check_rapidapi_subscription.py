"""
Check RapidAPI Subscription Status for LinkedIn Data API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_subscription():
    """Check if RapidAPI key is configured and test subscription"""
    
    api_key = os.getenv("RAPIDAPI_KEY")
    
    if not api_key:
        print("❌ RAPIDAPI_KEY not found in .env file")
        return False
    
    print(f"✅ RAPIDAPI_KEY found: {api_key[:20]}...")
    
    # Test the LinkedIn Data API
    url = "https://linkedin-data-api.p.rapidapi.com/get-profile-posts"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
    }
    params = {"username": "test"}
    
    print("\n🔍 Testing LinkedIn Data API subscription...")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 403:
            error_data = response.json() if response.content else {}
            print(f"\n❌ Subscription Error ({response.status_code})")
            print(f"Response: {error_data}")
            print("\n📋 To fix this:")
            print("1. Go to https://rapidapi.com/")
            print("2. Log in with your account")
            print("3. Search for 'LinkedIn Data API'")
            print("4. Click 'Subscribe' and choose a plan (check for free tier!)")
            print("5. Once subscribed, try again")
            return False
        
        elif response.status_code == 429:
            print(f"\n⚠️  Rate Limit Error ({response.status_code})")
            print("You've hit the API request limit.")
            print("This might mean:")
            print("- You've made too many requests (wait a few minutes)")
            print("- Your subscription tier has limited requests/month")
            print("- You need to subscribe to the API first")
            return False
        
        elif response.status_code == 200:
            print(f"\n✅ API is working! ({response.status_code})")
            data = response.json()
            if isinstance(data, dict) and 'data' in data:
                print(f"   Found {len(data.get('data', []))} posts")
            return True
        
        else:
            print(f"\n⚠️  Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RapidAPI LinkedIn Data API Subscription Checker")
    print("=" * 60)
    
    success = check_subscription()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Your LinkedIn tool is ready to use!")
    else:
        print("❌ Please subscribe to the LinkedIn Data API on RapidAPI")

