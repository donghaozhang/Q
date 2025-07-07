// Authentication Test Script
// Run this in browser console at http://localhost:3000

console.log("🔍 Starting Authentication Debug...");

// Test 1: Check if user is logged in
async function checkAuthStatus() {
    console.log("\n=== TEST 1: Authentication Status ===");
    
    try {
        // Check if Supabase is available
        if (typeof window !== 'undefined' && window.supabase) {
            console.log("✅ Supabase client available");
            
            const { data: { session }, error } = await window.supabase.auth.getSession();
            
            if (error) {
                console.error("❌ Session error:", error);
                return false;
            }
            
            if (session) {
                console.log("✅ User is logged in");
                console.log("📄 Session:", {
                    user_id: session.user?.id,
                    email: session.user?.email,
                    access_token: session.access_token ? "Present" : "Missing",
                    expires_at: new Date(session.expires_at * 1000),
                    token_preview: session.access_token?.substring(0, 20) + "..."
                });
                return session;
            } else {
                console.log("❌ No active session found");
                return false;
            }
        } else {
            console.error("❌ Supabase client not available in window");
            return false;
        }
    } catch (err) {
        console.error("❌ Error checking auth status:", err);
        return false;
    }
}

// Test 2: Test API call with authentication
async function testApiCall(session) {
    console.log("\n=== TEST 2: API Authentication Test ===");
    
    if (!session || !session.access_token) {
        console.error("❌ No session or access token available");
        return false;
    }
    
    try {
        // Test the health endpoint first (no auth required)
        const healthResponse = await fetch("http://localhost:8000/api/health");
        const healthData = await healthResponse.json();
        console.log("✅ Backend health check:", healthData);
        
        // Test an authenticated endpoint
        const authResponse = await fetch("http://localhost:8000/api/user/profile", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${session.access_token}`,
                "Content-Type": "application/json"
            }
        });
        
        console.log("🔐 Auth API Response Status:", authResponse.status);
        
        if (authResponse.status === 401) {
            console.error("❌ 401 Unauthorized - Token may be invalid or expired");
            
            // Try to decode the JWT to see what's in it
            try {
                const tokenParts = session.access_token.split('.');
                const payload = JSON.parse(atob(tokenParts[1]));
                console.log("📋 Token payload:", {
                    sub: payload.sub,
                    exp: new Date(payload.exp * 1000),
                    iss: payload.iss,
                    aud: payload.aud
                });
                
                if (payload.exp < Date.now() / 1000) {
                    console.error("❌ Token is expired!");
                } else {
                    console.log("✅ Token is not expired");
                }
            } catch (jwtErr) {
                console.error("❌ Error decoding JWT:", jwtErr);
            }
            
            return false;
        } else if (authResponse.ok) {
            console.log("✅ Authentication successful");
            return true;
        } else {
            console.error("❌ API call failed:", authResponse.status, authResponse.statusText);
            return false;
        }
        
    } catch (err) {
        console.error("❌ Error testing API call:", err);
        return false;
    }
}

// Test 3: Test agent initiate specifically
async function testAgentInitiate(session) {
    console.log("\n=== TEST 3: Agent Initiate Test ===");
    
    if (!session || !session.access_token) {
        console.error("❌ No session or access token available");
        return false;
    }
    
    try {
        const formData = new FormData();
        formData.append('prompt', 'Hello, test message');
        
        const response = await fetch("http://localhost:8000/api/agent/initiate", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${session.access_token}`
                // Don't set Content-Type for FormData
            },
            body: formData
        });
        
        console.log("🤖 Agent Initiate Response Status:", response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log("✅ Agent initiate successful:", data);
            return true;
        } else {
            const errorText = await response.text();
            console.error("❌ Agent initiate failed:", response.status, errorText);
            return false;
        }
        
    } catch (err) {
        console.error("❌ Error testing agent initiate:", err);
        return false;
    }
}

// Main test function
async function runAuthTests() {
    console.log("🚀 Running comprehensive authentication tests...\n");
    
    const session = await checkAuthStatus();
    
    if (session) {
        await testApiCall(session);
        await testAgentInitiate(session);
    } else {
        console.log("\n🔧 SOLUTION: User needs to log in first");
        console.log("1. Go to /auth to log in");
        console.log("2. Or check browser console for authentication errors");
    }
    
    console.log("\n✅ Authentication test complete!");
}

// Auto-run the tests
runAuthTests();