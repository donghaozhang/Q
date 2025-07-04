#!/usr/bin/env python3
"""
Quick script to set feature flags using the backend's flag system
"""
import asyncio
from flags.flags import set_flag

async def main():
    """Set the custom_agents flag to enabled"""
    try:
        result = await set_flag("custom_agents", True, "Enable custom agents feature")
        print(f"Setting custom_agents flag: {result}")
        
        # Verify it was set
        from flags.flags import is_enabled, get_flag_details
        enabled = await is_enabled("custom_agents")
        details = await get_flag_details("custom_agents")
        
        print(f"Flag enabled: {enabled}")
        print(f"Flag details: {details}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())