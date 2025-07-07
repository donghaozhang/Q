#!/bin/bash

# Robust service startup script for Q platform
set -e

echo "🚀 Starting Q Platform Services..."

# Kill any existing sessions
tmux kill-server 2>/dev/null || true

# Wait a moment
sleep 2

# Start backend API
echo "Starting Backend API..."
tmux new-session -d -s backend-api -c /home/zdhpe/suna/Q/backend \
  'echo "Backend API starting..."; uv run python api.py'

# Start backend worker
echo "Starting Backend Worker..."
tmux new-session -d -s backend-worker -c /home/zdhpe/suna/Q/backend \
  'echo "Backend Worker starting..."; uv run dramatiq --processes 2 --threads 2 run_agent_background'

# Start frontend with proper settings
echo "Starting Frontend..."
tmux new-session -d -s frontend -c /home/zdhpe/suna/Q/frontend \
  'export NODE_ENV=development; export NEXT_TELEMETRY_DISABLED=1; export NODE_OPTIONS="--max-old-space-size=2048"; echo "Frontend starting..."; npm run dev'

# Wait for services to start
echo "Waiting for services to initialize..."
sleep 10

# Check services
echo "Checking service status..."

# Check backend
if curl -s http://localhost:8000/api/health >/dev/null; then
    echo "✅ Backend API: OK"
else
    echo "❌ Backend API: Failed"
fi

# Check frontend (with retries)
FRONTEND_OK=false
for i in {1..5}; do
    if curl -s --max-time 5 http://localhost:3000 >/dev/null; then
        echo "✅ Frontend: OK"
        FRONTEND_OK=true
        break
    else
        echo "⏳ Frontend: Waiting... (attempt $i/5)"
        sleep 5
    fi
done

if [ "$FRONTEND_OK" = false ]; then
    echo "❌ Frontend: Failed to start"
fi

# Show sessions
echo ""
echo "Active tmux sessions:"
tmux list-sessions

echo ""
echo "🎉 Services started! Access the platform at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "To monitor logs:"
echo "   tmux attach -t frontend"
echo "   tmux attach -t backend-api"
echo "   tmux attach -t backend-worker"