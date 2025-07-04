#!/usr/bin/env node

/**
 * Test script to simulate the frontend agent creation flow
 * This mimics what the frontend does when trying to access agents
 */

async function testFeatureFlag() {
  try {
    console.log('🔍 Testing feature flag endpoint...');
    const response = await fetch('http://localhost:8000/api/feature-flags/custom_agents');
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('✅ Feature flag response:', JSON.stringify(data, null, 2));
    
    if (data.enabled !== true) {
      throw new Error('❌ Custom agents feature flag is not enabled!');
    }
    
    console.log('✅ Custom agents feature flag is ENABLED');
    return true;
  } catch (error) {
    console.error('❌ Feature flag test failed:', error.message);
    return false;
  }
}

async function testAgentsEndpoint() {
  try {
    console.log('\n🔍 Testing agents list endpoint (without auth)...');
    const response = await fetch('http://localhost:8000/api/agents');
    
    console.log(`📡 Response status: ${response.status} ${response.statusText}`);
    
    if (response.status === 401 || response.status === 403) {
      console.log('✅ Authentication required (expected behavior)');
      return true;
    } else if (response.status === 200) {
      const data = await response.json();
      console.log('✅ Agents endpoint accessible:', Object.keys(data));
      return true;
    } else {
      const error = await response.text();
      console.log('❓ Unexpected response:', error);
      return false;
    }
  } catch (error) {
    console.error('❌ Agents endpoint test failed:', error.message);
    return false;
  }
}

async function main() {
  console.log('🚀 Testing Frontend → Backend Agent Flow');
  console.log('=====================================\n');
  
  const flagTest = await testFeatureFlag();
  const agentsTest = await testAgentsEndpoint();
  
  console.log('\n📊 Test Results:');
  console.log('================');
  console.log(`Feature Flag: ${flagTest ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Agents API: ${agentsTest ? '✅ PASS' : '❌ FAIL'}`);
  
  if (flagTest && agentsTest) {
    console.log('\n🎉 SUCCESS: Frontend → Backend connection is working!');
    console.log('The "Custom agents is not enabled" error should be resolved.');
  } else {
    console.log('\n💥 FAILURE: Issues detected in frontend → backend flow');
  }
}

main().catch(console.error);