#!/usr/bin/env python3
"""
Debug feature flags by testing Redis connection and values
"""
import asyncio
import os
import sys
sys.path.append('/home/zdhpe/suna/Q/backend')

async def test_redis_connection():
    """Test Redis connection and feature flag values"""
    try:
        # Import the Redis service
        from services import redis
        
        print("Testing Redis connection...")
        client = await redis.get_client()
        
        # Test basic connection
        await client.ping()
        print("✓ Redis connection successful")
        
        # Check feature flag value
        flag_key = "feature_flag:custom_agents"
        enabled_value = await client.hget(flag_key, 'enabled')
        print(f"✓ custom_agents enabled value: {enabled_value}")
        
        # Test the feature flag function directly
        from flags.flags import is_enabled
        is_flag_enabled = await is_enabled('custom_agents')
        print(f"✓ is_enabled('custom_agents'): {is_flag_enabled}")
        
        # List all feature flags
        flag_list_key = "feature_flags:list"
        all_flags = await client.smembers(flag_list_key)
        print(f"✓ All feature flags: {all_flags}")
        
        # Test the flag manager directly
        from flags.flags import get_flag_manager
        manager = get_flag_manager()
        all_flags_dict = await manager.list_flags()
        print(f"✓ All flags via manager: {all_flags_dict}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Set up environment
    from dotenv import load_dotenv
    load_dotenv('/home/zdhpe/suna/Q/backend/.env')
    
    asyncio.run(test_redis_connection())