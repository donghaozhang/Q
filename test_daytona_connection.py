#!/usr/bin/env python3
"""
Test script to debug Daytona sandbox creation
"""
import os
import sys
sys.path.append('/home/zdhpe/suna/Q/backend')

from dotenv import load_dotenv
load_dotenv('/home/zdhpe/suna/Q/backend/.env')

from daytona_sdk import Daytona, DaytonaConfig
import uuid

def test_daytona_connection():
    """Test basic Daytona connection and configuration"""
    print("🔍 Testing Daytona Connection")
    print("=" * 40)
    
    # Check environment variables
    api_key = os.getenv('DAYTONA_API_KEY')
    server_url = os.getenv('DAYTONA_SERVER_URL')
    target = os.getenv('DAYTONA_TARGET')
    
    print(f"API Key: {'✅ Present' if api_key else '❌ Missing'}")
    print(f"Server URL: {server_url}")
    print(f"Target: {target}")
    
    if not api_key:
        print("❌ DAYTONA_API_KEY is missing!")
        return False
    
    try:
        # Initialize Daytona client
        print("\n🔧 Initializing Daytona client...")
        config = DaytonaConfig(
            api_key=api_key,
            server_url=server_url,
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error with Daytona connection: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_sandbox_creation():
    """Test sandbox creation with minimal parameters"""
    print("\n🚀 Testing Sandbox Creation")
    print("=" * 40)
    
    try:
        from sandbox.sandbox import create_sandbox
        
        # Generate test password
        test_password = str(uuid.uuid4())[:8]
        test_project_id = f"test-{uuid.uuid4()}"[:20]
        
        print(f"Test password: {test_password}")
        print(f"Test project ID: {test_project_id}")
        
        print("\n🔧 Creating sandbox...")
        sandbox = create_sandbox(test_password, test_project_id)
        
        print(f"✅ Sandbox created successfully!")
        print(f"  - ID: {sandbox.id}")
        print(f"  - State: {sandbox.state}")
        
        # Clean up test sandbox
        print(f"\n🧹 Cleaning up test sandbox...")
        from sandbox.sandbox import delete_sandbox
        delete_sandbox(sandbox.id)
        print("✅ Test sandbox deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Sandbox creation failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def main():
    print("🧪 Daytona Sandbox Debug Test")
    print("="*50)
    
    connection_ok = test_daytona_connection()
    
    if connection_ok:
        creation_ok = test_sandbox_creation()
        
        print("\n📊 Test Results:")
        print("=" * 20)
        print(f"Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
        print(f"Creation: {'✅ PASS' if creation_ok else '❌ FAIL'}")
        
        if connection_ok and creation_ok:
            print("\n🎉 All tests passed! Sandbox service is working.")
        else:
            print("\n💥 Tests failed. Check configuration and Daytona service.")
    else:
        print("\n💥 Connection failed. Cannot proceed with creation test.")

if __name__ == "__main__":
    main()