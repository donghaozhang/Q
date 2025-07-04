#!/usr/bin/env python3
"""
Test script to debug Daytona sandbox creation with fixed configuration
"""
import os
import sys
sys.path.append('/home/zdhpe/suna/Q/backend')

from dotenv import load_dotenv
load_dotenv('/home/zdhpe/suna/Q/backend/.env')

from daytona_sdk import Daytona, DaytonaConfig
import uuid

def test_daytona_with_fixed_config():
    """Test Daytona connection with corrected configuration"""
    print("🔍 Testing Daytona with Fixed Configuration")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv('DAYTONA_API_KEY')
    server_url = os.getenv('DAYTONA_SERVER_URL')
    target = os.getenv('DAYTONA_TARGET')
    
    print(f"API Key: {'✅ Present' if api_key else '❌ Missing'}")
    print(f"Original Server URL: {server_url}")
    print(f"Target: {target}")
    
    if not api_key:
        print("❌ DAYTONA_API_KEY is missing!")
        return False
    
    try:
        # Try with api_url instead of server_url
        print("\n🔧 Initializing Daytona client with api_url...")
        config = DaytonaConfig(
            api_key=api_key,
            api_url=server_url,  # Use api_url instead of server_url
            target=target
        )
        
        client = Daytona(config)
        print("✅ Daytona client initialized successfully")
        
        # Test listing sandboxes
        print("\n📋 Testing sandbox listing...")
        sandboxes = client.list()
        print(f"✅ Found {len(sandboxes)} existing sandboxes")
        
        for sandbox in sandboxes[:3]:  # Show first 3
            print(f"  - {sandbox.id}: {sandbox.state}")
        
        return True, client
        
    except Exception as e:
        print(f"❌ Error with fixed config: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        # Try with minimal config
        try:
            print("\n🔧 Trying with minimal configuration...")
            config = DaytonaConfig(api_key=api_key)
            client = Daytona(config)
            sandboxes = client.list()
            print(f"✅ Minimal config works! Found {len(sandboxes)} sandboxes")
            return True, client
            
        except Exception as e2:
            print(f"❌ Minimal config also failed: {str(e2)}")
            return False, None

def test_http_client_fix():
    """Test if we can work around the HTTP client issue"""
    print("\n🔧 Testing HTTP Client Workaround")
    print("=" * 40)
    
    try:
        # Try downgrading urllib3 or using different HTTP settings
        import urllib3
        print(f"urllib3 version: {urllib3.__version__}")
        
        # Check if we can disable SSL warnings temporarily
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Now try the connection
        return test_daytona_with_fixed_config()
        
    except Exception as e:
        print(f"❌ HTTP client workaround failed: {str(e)}")
        return False, None

def main():
    print("🧪 Daytona Fixed Configuration Test")
    print("="*50)
    
    # First try with fixed config
    success, client = test_daytona_with_fixed_config()
    
    if not success:
        # Try HTTP client fix
        print("\n🔄 Trying HTTP client workaround...")
        success, client = test_http_client_fix()
    
    print("\n📊 Test Results:")
    print("=" * 20)
    print(f"Connection: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 Connection successful! The issue was the configuration.")
        print("💡 Solution: Use api_url instead of server_url in DaytonaConfig")
    else:
        print("\n💥 Connection still failing. May need SDK upgrade or different approach.")
        print("\n💡 Possible solutions:")
        print("   1. Upgrade daytona-sdk package")
        print("   2. Use HTTP client fallback") 
        print("   3. Implement local sandbox alternative")

if __name__ == "__main__":
    main()