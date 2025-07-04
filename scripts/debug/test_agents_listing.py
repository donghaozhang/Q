#!/usr/bin/env python3
"""
Test script to check agents listing endpoint with proper authentication
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/zdhpe/suna/Q/backend/.env')

def get_auth_token():
    """Get authentication token using Supabase auth"""
    # For testing, we'll use the Supabase anon key
    # In production, this would be a proper user JWT token
    anon_key = os.getenv('SUPABASE_ANON_KEY')
    if not anon_key:
        print("❌ SUPABASE_ANON_KEY not found in environment")
        return None
    
    # This is a simplified test - in reality, you'd get a proper user JWT
    # For now, we'll just check if the endpoint is accessible
    return anon_key

def test_agents_listing_with_auth():
    """Test the agents listing endpoint with authentication"""
    print("🧪 Testing Agents Listing Endpoint")
    print("=" * 40)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("❌ Could not get authentication token")
        return False
    
    # Test endpoint
    url = "http://localhost:8000/api/agents"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"📡 Testing GET {url}")
    print(f"🔑 Using auth header: Bearer <token>")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('agents', []))} agents")
            print(f"📋 Response: {json.dumps(data, indent=2)}")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed (401)")
            print(f"📋 Response: {response.text}")
            return False
        elif response.status_code == 403:
            print("❌ Forbidden (403) - Feature might be disabled")
            print(f"📋 Response: {response.text}")
            return False
        elif response.status_code == 500:
            print("❌ Server Error (500)")
            try:
                error_data = response.json()
                print(f"📋 Error Details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📋 Response: {response.text}")
            return False
        else:
            print(f"❓ Unexpected status code: {response.status_code}")
            print(f"📋 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_feature_flags():
    """Test if custom_agents feature flag is enabled"""
    print("\n🔍 Testing Feature Flags")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/api/feature-flags/custom_agents", timeout=5)
        if response.status_code == 200:
            data = response.json()
            enabled = data.get('enabled', False)
            print(f"Custom Agents Feature Flag: {'✅ ENABLED' if enabled else '❌ DISABLED'}")
            return enabled
        else:
            print(f"❌ Could not check feature flag: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking feature flag: {str(e)}")
        return False

def main():
    print("🚀 Agents Listing Test")
    print("="*50)
    
    # First check if backend is healthy
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code != 200:
            print("💥 Backend is not responding. Cannot proceed with tests.")
            return
    except:
        print("💥 Backend is not responding. Cannot proceed with tests.")
        return
    
    # Check feature flags
    feature_enabled = test_feature_flags()
    
    if not feature_enabled:
        print("\n💥 Custom agents feature is disabled. This explains the 500 error!")
        print("The backend needs to enable this feature flag.")
        return
    
    # Test agents listing
    success = test_agents_listing_with_auth()
    
    print("\n📊 Test Results:")
    print("=" * 20)
    print(f"Feature Flag: {'✅ PASS' if feature_enabled else '❌ FAIL'}")
    print(f"Agents Listing: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 SUCCESS: Agents listing endpoint is working!")
    else:
        print("\n💥 FAILURE: Agents listing endpoint has issues.")

if __name__ == "__main__":
    main()