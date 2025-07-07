#!/bin/bash
# Start all Suna services in new terminal windows

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting all Suna (Q) services...${NC}"

# Check if infrastructure is running
if ! docker compose ps | grep -q "Up"; then
    echo -e "${YELLOW}Starting infrastructure first...${NC}"
    docker compose up -d redis rabbitmq
    sleep 5
fi

# Open Windows Terminal tabs
if command -v cmd.exe &> /dev/null; then
    echo -e "${YELLOW}Opening Windows Terminal tabs...${NC}"
    
    # Frontend
    cmd.exe /c "wt -w 0 new-tab --title \"Frontend\" --suppressApplicationTitle wsl.exe -d $WSL_DISTRO_NAME bash -c \"cd $(pwd)/frontend && npm run dev; exec bash\""
    
    # Backend API
    cmd.exe /c "wt -w 0 new-tab --title \"Backend API\" --suppressApplicationTitle wsl.exe -d $WSL_DISTRO_NAME bash -c \"cd $(pwd)/backend && ~/.local/bin/uv run python api.py; exec bash\""
    
    # Worker
    cmd.exe /c "wt -w 0 new-tab --title \"Worker\" --suppressApplicationTitle wsl.exe -d $WSL_DISTRO_NAME bash -c \"cd $(pwd)/backend && ~/.local/bin/uv run dramatiq run_agent_background; exec bash\""
    
    echo -e "${GREEN}✅ All services starting in Windows Terminal tabs${NC}"
else
    # Fallback - just show commands
    echo -e "${YELLOW}Please run these commands in separate terminals:${NC}"
    echo -e "${BLUE}Frontend:${NC} cd frontend && npm run dev"
    echo -e "${BLUE}Backend:${NC} cd backend && ~/.local/bin/uv run python api.py"
    echo -e "${BLUE}Worker:${NC} cd backend && ~/.local/bin/uv run dramatiq run_agent_background"
fi

echo -e "\n${YELLOW}URLs will be available at:${NC}"
echo -e "🌐 Frontend: http://localhost:3000"
echo -e "📊 Backend API: http://localhost:8000/docs"

# Wait and open browser
echo -e "\n${YELLOW}Waiting for services to start...${NC}"
sleep 10

# Try to open browser
if command -v cmd.exe &> /dev/null; then
    cmd.exe /c start http://localhost:3000 2>/dev/null || true
fi