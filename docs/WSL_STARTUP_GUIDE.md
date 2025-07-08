# Suna/Q WSL Startup Guide

**Date**: July 8, 2025  
**Platform**: WSL2 with Docker Desktop on Windows  
**Status**: ✅ WORKING

## Overview

This guide provides step-by-step instructions for starting Suna/Q in WSL2 and accessing it from Windows Chrome browser.

## Prerequisites

- WSL2 installed and configured
- Docker Desktop running on Windows with WSL2 integration enabled
- Chrome browser (Windows or WSL)

## Quick Start

### Option 1: Automated Script
```bash
# Make script executable and run
chmod +x scripts/start-suna-wsl.sh
./scripts/start-suna-wsl.sh
```

### Option 2: Manual Commands
```bash
# 1. Navigate to project directory
cd /home/zdhpe/suna/Q

# 2. Start all services with Docker Compose
docker compose up -d

# 3. Verify services are running
docker compose ps

# 4. Check service logs (optional)
docker compose logs -f backend worker

# 5. Open browser (choose one):
# Option A: From Windows - Open Chrome and go to http://localhost:3000
# Option B: From WSL
google-chrome http://localhost:3000 &
```

## Service Details

### Core Services
- **Frontend**: Next.js app on port 3000
- **Backend**: FastAPI on port 8000  
- **Worker**: Dramatiq background worker for agent execution
- **Redis**: Session storage and caching on port 6379
- **RabbitMQ**: Task queue on port 5672

### Service Status Check
```bash
# Check all services
docker compose ps

# Health check backend
curl http://localhost:8000/api/health

# Check frontend
curl -I http://localhost:3000

# View service logs
docker compose logs backend --tail=20
docker compose logs worker --tail=20
```

## Network Access

### From Windows
- **Primary URL**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **RabbitMQ Management**: http://localhost:15672

### From WSL (if needed)
- **WSL IP**: http://172.26.67.88:3000 (IP may vary)
- **Localhost**: http://localhost:3000

## Browser Options

### Windows Chrome (Recommended)
1. Open Chrome on Windows
2. Navigate to: `http://localhost:3000`
3. Sign up/login to access agent functionality

### WSL Chrome
```bash
# Check if Chrome is available
which google-chrome

# Open from WSL terminal
google-chrome http://localhost:3000 &

# Or use chromium if available
chromium-browser http://localhost:3000 &
```

## Troubleshooting

### Services Not Starting
```bash
# Check Docker is running
docker --version

# Check WSL2 integration
docker context ls

# Restart all services
docker compose down
docker compose up -d
```

### Port Conflicts
```bash
# Check what's using ports
ss -tlnp | grep 3000
ss -tlnp | grep 8000

# Kill conflicting processes
pkill -f "npm run dev"
pkill -f "python api.py"
```

### Browser Access Issues
```bash
# Check if ports are accessible from Windows
# From Windows Command Prompt:
# curl http://localhost:3000
# curl http://localhost:8000/api/health

# Alternative: Use WSL IP from Windows
# http://172.26.67.88:3000
```

### Service Logs
```bash
# View all logs
docker compose logs

# Follow specific service
docker compose logs -f backend
docker compose logs -f worker
docker compose logs -f frontend

# Filter by time
docker compose logs --since 5m worker
```

## Stopping Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (full cleanup)
docker compose down -v

# Stop specific service
docker compose stop backend
```

## Important Files

- **Docker Compose**: `docker-compose.yml`
- **Environment Config**: `backend/.env` (contains API keys)
- **Startup Script**: `scripts/start-suna-wsl.sh`
- **Setup Wizard**: `python setup.py`
- **Manual Start**: `python start.py`

## Agent Testing

Once the platform is running:

1. **Access**: http://localhost:3000
2. **Sign Up**: Create account with email/password
3. **Create Agent**: Use the agent builder interface
4. **Test Response**: Send message "What is 2+2?" to verify fixes work
5. **Verify**: Agent should respond with visible answer

## Performance Tips

### WSL2 Performance
- Store code in WSL filesystem (`/home/user/`) not Windows mount (`/mnt/c/`)
- Use WSL2 with sufficient memory allocation
- Keep Docker Desktop updated

### Development Workflow
```bash
# Fast restart after code changes
docker compose restart backend worker

# Rebuild containers after dependency changes
docker compose build backend worker
docker compose up -d

# Watch logs during development
docker compose logs -f backend worker
```

## Automation

The provided startup script (`scripts/start-suna-wsl.sh`) handles:
- Service startup verification
- Port conflict detection
- Browser launching
- Error reporting
- Service health checks

Use this for consistent, reliable startup experience.