#!/bin/bash

# Stable frontend startup script for Q platform
# This script will automatically restart the frontend if it crashes

FRONTEND_DIR="/home/zdhpe/suna/Q/frontend"
SESSION_NAME="frontend-stable"
MAX_RETRIES=5
RETRY_COUNT=0

echo "Starting stable frontend service..."
cd "$FRONTEND_DIR"

# Function to start frontend
start_frontend() {
    echo "$(date): Starting frontend (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)"
    
    # Kill any existing session
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null
    
    # Start new session
    tmux new-session -d -s "$SESSION_NAME" -c "$FRONTEND_DIR" "
        echo 'Frontend starting at $(date)';
        npm run dev;
        echo 'Frontend exited at $(date)';
        read -p 'Press Enter to continue...'
    "
    
    # Wait for startup
    sleep 15
    
    # Check if it's running
    if curl -s http://localhost:3000 >/dev/null; then
        echo "$(date): Frontend started successfully"
        RETRY_COUNT=0
        return 0
    else
        echo "$(date): Frontend failed to start"
        return 1
    fi
}

# Function to monitor and restart
monitor_frontend() {
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if ! curl -s http://localhost:3000 >/dev/null; then
            echo "$(date): Frontend is down, restarting..."
            RETRY_COUNT=$((RETRY_COUNT + 1))
            
            if start_frontend; then
                echo "$(date): Frontend restarted successfully"
            else
                echo "$(date): Failed to restart frontend"
                if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
                    echo "$(date): Max retries reached, giving up"
                    break
                fi
            fi
        fi
        
        # Check every 30 seconds
        sleep 30
    done
}

# Initial start
if start_frontend; then
    echo "Frontend is running at http://localhost:3000"
    echo "Monitoring for crashes... (Ctrl+C to stop)"
    monitor_frontend
else
    echo "Failed to start frontend"
    exit 1
fi