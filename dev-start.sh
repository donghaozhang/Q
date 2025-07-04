#!/bin/bash
# Development start script - Infrastructure in Docker, Apps run locally

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Suna (Q) Development Mode${NC}"
echo -e "${BLUE}=============================${NC}\n"
echo -e "${YELLOW}This starts infrastructure in Docker and runs apps locally (fastest)${NC}\n"

# Check Docker
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker Desktop is not running${NC}"
    echo -e "${YELLOW}Please start Docker Desktop on Windows first${NC}"
    exit 1
fi

# Check environment files
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ backend/.env not found${NC}"
    echo -e "${YELLOW}Run 'python setup.py' first${NC}"
    exit 1
fi

# Start only infrastructure services
echo -e "${YELLOW}Starting infrastructure services (Redis, RabbitMQ)...${NC}"
docker compose up -d redis rabbitmq

# Wait for services
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 5

# Check service health
docker compose ps redis rabbitmq

echo -e "\n${GREEN}✅ Infrastructure is ready!${NC}"
echo -e "\n${YELLOW}Now start the applications in separate terminals:${NC}\n"

echo -e "${BLUE}Terminal 1 - Frontend:${NC}"
echo -e "cd frontend"
echo -e "npm install  # (first time only)"
echo -e "npm run dev"
echo -e ""

echo -e "${BLUE}Terminal 2 - Backend API:${NC}"
echo -e "cd backend"
echo -e "uv sync  # (first time only)"
echo -e "uv run python api.py"
echo -e ""

echo -e "${BLUE}Terminal 3 - Worker (optional):${NC}"
echo -e "cd backend"
echo -e "uv run dramatiq run_agent_background"
echo -e ""

echo -e "${YELLOW}URLs:${NC}"
echo -e "🌐 Frontend: http://localhost:3000"
echo -e "📊 Backend: http://localhost:8000/docs"
echo -e ""

echo -e "${YELLOW}To stop infrastructure:${NC} docker compose down"

# Optional: Open new terminal windows
if command -v gnome-terminal &> /dev/null; then
    read -p "Open terminal windows for you? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gnome-terminal --tab --title="Frontend" --working-directory="$PWD/frontend" -- bash -c "npm run dev; bash"
        gnome-terminal --tab --title="Backend" --working-directory="$PWD/backend" -- bash -c "uv run python api.py; bash"
    fi
elif command -v cmd.exe &> /dev/null; then
    echo -e "\n${YELLOW}💡 Tip: You can open Windows Terminal tabs with:${NC}"
    echo "wt -w 0 nt -d frontend --title Frontend"
    echo "wt -w 0 nt -d backend --title Backend"
fi