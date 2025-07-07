#!/bin/bash
# Fast build script for WSL development

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Fast Build for Suna (Q)${NC}"
echo -e "${BLUE}===========================${NC}\n"

# Option to use optimized files
USE_OPTIMIZED=false
if [[ "$1" == "--optimized" ]]; then
    USE_OPTIMIZED=true
    echo -e "${YELLOW}Using optimized Dockerfile and requirements${NC}"
fi

# Clean up any running containers
echo -e "${YELLOW}Cleaning up existing containers...${NC}"
docker compose down 2>/dev/null || true

# Build strategy selection
if [ "$USE_OPTIMIZED" = true ]; then
    # Use optimized files
    echo -e "${YELLOW}Temporarily replacing files with optimized versions...${NC}"
    
    # Backup originals
    cp backend/Dockerfile backend/Dockerfile.original
    cp backend/requirements.txt backend/requirements.original.txt
    
    # Use optimized versions
    cp backend/Dockerfile.optimized backend/Dockerfile
    cp backend/requirements-pinned.txt backend/requirements.txt
    
    # Build
    echo -e "${YELLOW}Building with optimized configuration...${NC}"
    docker compose build --parallel
    
    # Restore originals
    mv backend/Dockerfile.original backend/Dockerfile
    mv backend/requirements.original.txt backend/requirements.txt
    
    echo -e "${GREEN}✅ Build complete with optimized files${NC}"
else
    # Regular build with some optimizations
    echo -e "${YELLOW}Building with Docker BuildKit optimizations...${NC}"
    
    # Enable BuildKit for faster builds
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    
    # Build with parallelism
    docker compose build --parallel
    
    echo -e "${GREEN}✅ Build complete${NC}"
fi

# Start services
echo -e "\n${YELLOW}Starting services...${NC}"
docker compose up -d

# Wait for services
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Check status
echo -e "\n${BLUE}Service Status:${NC}"
docker compose ps

echo -e "\n${GREEN}✨ Suna is starting up!${NC}"
echo -e "${BLUE}🌐 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}📊 Backend API: http://localhost:8000/docs${NC}"
echo -e "${BLUE}📝 View logs: docker compose logs -f${NC}"
echo -e "${BLUE}🛑 Stop services: docker compose down${NC}"

# Tips
echo -e "\n${YELLOW}💡 Build Tips:${NC}"
echo -e "- Use ${GREEN}--optimized${NC} flag for faster builds with pinned dependencies"
echo -e "- First build is slow, subsequent builds use cache"
echo -e "- For development, consider running services manually (no Docker)"