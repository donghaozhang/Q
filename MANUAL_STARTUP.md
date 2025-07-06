# Manual Service Startup Guide

This guide documents how to manually start all Suna (Q) services locally using `uv` and `npm`.

## Prerequisites

- Ensure all dependencies are installed
- Activate the backend virtual environment if needed
- Check that required environment variables are set in `.env` files

## Starting Services

### 1. Backend API Server

Start the FastAPI backend server:

```bash
cd /home/zdhpe/suna/Q/backend
uv run python api.py
```

The API will be available at: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

### 2. Background Worker

Start the Dramatiq background worker for agent execution:

```bash
cd /home/zdhpe/suna/Q/backend
uv run dramatiq --processes 4 --threads 4 run_agent_background
```

This starts 4 worker processes with 4 threads each to handle background tasks.

### 3. Frontend Development Server

Start the Next.js frontend:

```bash
cd /home/zdhpe/suna/Q/frontend
npm run dev
```

The frontend will be available at: http://localhost:3000

## Using tmux for Service Management

To keep services running in the background, use tmux sessions:

```bash
# Start backend API in tmux
tmux new-session -d -s backend-api -c /home/zdhpe/suna/Q/backend 'uv run python api.py'

# Start background worker in tmux
tmux new-session -d -s backend-worker -c /home/zdhpe/suna/Q/backend 'uv run dramatiq --processes 4 --threads 4 run_agent_background'

# Start frontend in tmux
tmux new-session -d -s frontend-dev -c /home/zdhpe/suna/Q/frontend 'npm run dev'
```

### tmux Commands

- List sessions: `tmux list-sessions`
- Attach to session: `tmux attach -t <session-name>`
- Detach from session: `Ctrl+b, d`
- Switch between sessions: `Ctrl+b, s`
- Kill session: `tmux kill-session -t <session-name>`

## Verifying Services

Check that all services are running:

```bash
# Check backend health
curl http://localhost:8000/api/health

# Check listening ports
ss -tlnp | grep -E ":(8000|3000)"

# Check running processes
ps aux | grep -E "(npm|node|python api.py|dramatiq)" | grep -v grep
```

## Stopping Services

If using tmux:
```bash
tmux kill-session -t backend-api
tmux kill-session -t backend-worker
tmux kill-session -t frontend-dev
```

If running in terminal, use `Ctrl+C` to stop each service.

## Troubleshooting

1. **Port already in use**: Kill existing processes using the port
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Missing dependencies**: 
   - Backend: `cd backend && uv sync`
   - Frontend: `cd frontend && npm install`

3. **Environment variables**: Ensure `.env` files exist in both backend and frontend directories

4. **Frontend crashes**: If the frontend tmux session terminates, check for Node.js errors and ensure all npm dependencies are installed