#!/usr/bin/env python3
"""
Minimal backend to test feature flags without full dependency resolution
"""

import os
import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Minimal Q Backend", version="0.1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection - try different hosts
redis_client = None
hosts_to_try = ['redis', 'localhost', '127.0.0.1']

for host in hosts_to_try:
    try:
        test_client = redis.Redis(host=host, port=6379, decode_responses=True)
        test_client.ping()
        redis_client = test_client
        print(f"✅ Connected to Redis at {host}")
        break
    except Exception as e:
        print(f"❌ Redis connection failed for {host}: {e}")
        continue

if redis_client is None:
    print("❌ Could not connect to Redis on any host")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "redis_connected": redis_client is not None,
        "message": "Minimal Q Backend is running"
    }

@app.get("/api/feature-flags/{flag_name}")
async def get_feature_flag(flag_name: str):
    """Get a specific feature flag"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not available")
    
    try:
        # Check with feature_flag: prefix
        flag_key = f"feature_flag:{flag_name}"
        flag_value = redis_client.get(flag_key)
        
        if flag_value is None:
            # Fallback to direct key
            flag_value = redis_client.get(flag_name)
        
        enabled = flag_value == "true" if flag_value else False
        
        return {
            "flag_name": flag_name,
            "enabled": enabled,
            "details": {
                "description": f"Feature flag for {flag_name}",
                "key_used": flag_key if redis_client.get(flag_key) else flag_name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving flag: {str(e)}")

@app.get("/api/feature-flags")
async def get_all_feature_flags():
    """Get all feature flags"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not available")
    
    try:
        # Get all feature_flag: prefixed keys
        flag_keys = redis_client.keys("feature_flag:*")
        flags = {}
        
        for key in flag_keys:
            flag_name = key.replace("feature_flag:", "")
            flag_value = redis_client.get(key)
            flags[flag_name] = flag_value == "true" if flag_value else False
        
        return {"flags": flags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving flags: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting minimal Q backend...")
    print("📍 Available endpoints:")
    print("   GET /api/health")
    print("   GET /api/feature-flags/{flag_name}")
    print("   GET /api/feature-flags")
    print("🌐 CORS enabled for localhost:3000")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )