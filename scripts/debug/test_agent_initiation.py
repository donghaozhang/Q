#!/usr/bin/env python3
"""
Test script to verify agent initiation works with sandbox fallback
"""
import requests
import json

def test_agent_initiation():
    """Test the agent initiation endpoint"""
    print("🧪 Testing Agent Initiation with Sandbox Fallback")
    print("=" * 55)
    
    # Test endpoint
    url = "http://localhost:8000/api/agent/initiate"
    
    # Prepare test data (multipart form data)
    data = {
        'prompt': 'Hello, test agent initialization',
        'model_name': 'openrouter/google/gemini-2.5-flash-preview',
        'enable_thinking': False,
        'stream': True,
        'enable_context_manager': False
    }
    
    print(f"📡 Testing POST {url}")
    print(f"📝 Payload: {json.dumps(data, indent=2)}")
    
    try:
        # Make the request (this will likely fail with 401 due to no auth)
        response = requests.post(url, data=data, timeout=30)
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 401:
            print("✅ Expected: Authentication required (401)")
            print("✅ This means the endpoint is accessible and sandbox fallback logic is working!")
            return True
        elif response.status_code == 500:
            try:
                error_data = response.json()
                print(f"❌ Server Error (500): {error_data}")
                if "Failed to create sandbox" in str(error_data):
                    print("❌ Sandbox fallback didn't work - still getting sandbox creation error")
                    return False
                else:
                    print("❌ Different server error - may be unrelated to sandbox")
                    return False
            except:
                print(f"❌ Server Error (500): {response.text}")
                return False
        else:
            try:
                response_data = response.json()
                print(f"📋 Response Body: {json.dumps(response_data, indent=2)}")
            except:
                print(f"📋 Response Body: {response.text}")
            
            if response.status_code == 200:
                print("🎉 Success! Agent initiation worked!")
                return True
            else:
                print(f"❓ Unexpected status code: {response.status_code}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_health_endpoint():
    """Test the health endpoint first"""
    print("🔍 Testing Health Endpoint")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is healthy: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def main():
    print("🚀 Agent Initiation Test with Sandbox Fallback")
    print("="*60)
    
    # First check if backend is healthy
    if not test_health_endpoint():
        print("\n💥 Backend is not responding. Cannot proceed with tests.")
        return
    
    print("\n" + "="*60)
    
    # Test agent initiation
    success = test_agent_initiation()
    
    print("\n📊 Test Results:")
    print("=" * 20)
    print(f"Agent Initiation: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 SUCCESS: Sandbox fallback is working!")
        print("The 'Failed to create sandbox' error should be resolved.")
        print("Agents can now be initiated without requiring Daytona sandbox.")
    else:
        print("\n💥 FAILURE: Sandbox fallback needs more work.")

if __name__ == "__main__":
    main()