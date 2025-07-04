# Debug Scripts

This folder contains debugging and testing utilities for troubleshooting the Q platform.

## Scripts Overview

### 🧪 Agent Testing
- **`test_agent_initiation.py`** - Tests agent initiation endpoint with sandbox fallback
  - Verifies sandbox fallback mechanism works
  - Tests endpoint returns proper status codes
  - Useful for debugging agent startup issues

- **`test_agents_listing.py`** - Tests agents listing endpoint with authentication
  - Verifies agents API endpoints
  - Tests feature flag functionality
  - Includes authentication token handling

### 🔧 Daytona/Sandbox Testing
- **`test_daytona_connection.py`** - Tests basic Daytona SDK connectivity
  - Verifies Daytona configuration
  - Tests sandbox listing functionality
  - Useful for debugging Daytona integration

- **`test_daytona_fixed.py`** - Tests Daytona with configuration fixes
  - Tests corrected Daytona configuration
  - Includes HTTP client workarounds
  - Helps debug urllib3 compatibility issues

## Usage

Run these scripts when troubleshooting specific issues:

```bash
# Test agent functionality
python3 scripts/debug/test_agent_initiation.py

# Test agents listing
python3 scripts/debug/test_agents_listing.py

# Test Daytona connectivity
python3 scripts/debug/test_daytona_connection.py
python3 scripts/debug/test_daytona_fixed.py
```

## Purpose

These scripts were created during the platform setup and fixing process to:
- Isolate and test specific functionality
- Verify fixes work correctly
- Provide reproducible test cases
- Help with future debugging

## Note

These are debugging utilities, not part of the main test suite. For proper unit/integration tests, see:
- Backend tests: `./backend/tests/`
- Frontend tests: Built into React/Next.js testing framework

---
*Created: 2025-07-04*