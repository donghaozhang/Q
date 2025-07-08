#!/bin/bash

# Suna/Q WSL Startup Script
# Date: July 8, 2025
# Purpose: Automated startup for Suna platform in WSL2 environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[SUNA]${NC} $1"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if ss -tlnp | grep ":$port " > /dev/null; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to check Docker
check_docker() {
    print_status "Checking Docker availability..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker Desktop on Windows."
        exit 1
    fi
    
    print_status "Docker is running ✓"
}

# Function to check for port conflicts
check_ports() {
    print_status "Checking for port conflicts..."
    
    local conflicts=0
    
    if check_port 3000; then
        print_warning "Port 3000 is already in use"
        conflicts=$((conflicts + 1))
    fi
    
    if check_port 8000; then
        print_warning "Port 8000 is already in use"
        conflicts=$((conflicts + 1))
    fi
    
    if [ $conflicts -gt 0 ]; then
        print_warning "Found $conflicts port conflicts. Attempting to stop existing services..."
        docker compose down 2>/dev/null || true
        sleep 2
    fi
    
    print_status "Port check completed"
}

# Function to start services
start_services() {
    print_status "Starting Suna services..."
    
    # Navigate to project directory
    cd /home/zdhpe/suna/Q
    
    # Start services
    if docker compose up -d; then
        print_status "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be ready
    print_status "Waiting for services to initialize..."
    sleep 10
}

# Function to verify services
verify_services() {
    print_status "Verifying service health..."
    
    local max_retries=30
    local retry_count=0
    
    # Check backend health
    while [ $retry_count -lt $max_retries ]; do
        if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
            print_status "Backend is healthy ✓"
            break
        fi
        
        retry_count=$((retry_count + 1))
        if [ $retry_count -eq $max_retries ]; then
            print_error "Backend health check failed after $max_retries attempts"
            return 1
        fi
        
        sleep 1
    done
    
    # Check frontend
    if curl -s -I http://localhost:3000 | grep "200 OK" > /dev/null; then
        print_status "Frontend is healthy ✓"
    else
        print_warning "Frontend may not be fully ready yet"
    fi
    
    # Show service status
    print_status "Service status:"
    docker compose ps
}

# Function to open browser
open_browser() {
    print_status "Opening browser..."
    
    # Check if we should open browser
    if [ "$1" = "--no-browser" ]; then
        print_status "Skipping browser launch (--no-browser flag)"
        return
    fi
    
    # Try to open Chrome from WSL
    if command -v google-chrome &> /dev/null; then
        print_status "Opening Chrome from WSL..."
        google-chrome http://localhost:3000 &> /dev/null &
    elif command -v chromium-browser &> /dev/null; then
        print_status "Opening Chromium from WSL..."
        chromium-browser http://localhost:3000 &> /dev/null &
    else
        print_warning "No browser found in WSL"
        print_status "Open Chrome on Windows and go to: http://localhost:3000"
    fi
}

# Function to show service info
show_info() {
    print_header "Suna/Q is now running!"
    echo ""
    echo -e "${GREEN}Access URLs:${NC}"
    echo "  Frontend:  http://localhost:3000"
    echo "  Backend:   http://localhost:8000"
    echo "  API Docs:  http://localhost:8000/docs"
    echo "  RabbitMQ:  http://localhost:15672"
    echo ""
    echo -e "${GREEN}From Windows:${NC}"
    echo "  Open Chrome and navigate to http://localhost:3000"
    echo ""
    echo -e "${GREEN}Useful Commands:${NC}"
    echo "  View logs:    docker compose logs -f"
    echo "  Stop all:     docker compose down"
    echo "  Restart:      docker compose restart backend worker"
    echo "  Service status: docker compose ps"
    echo ""
    
    # Get WSL IP for alternative access
    local wsl_ip=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
    echo -e "${BLUE}Alternative WSL IP:${NC} http://$wsl_ip:3000"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --no-browser    Don't automatically open browser"
    echo "  --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Start services and open browser"
    echo "  $0 --no-browser      # Start services without opening browser"
}

# Main execution
main() {
    print_header "Starting Suna/Q Platform in WSL2"
    echo ""
    
    # Parse arguments
    local open_browser_flag=true
    
    for arg in "$@"; do
        case $arg in
            --no-browser)
                open_browser_flag=false
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $arg"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Execute startup sequence
    check_docker
    check_ports
    start_services
    verify_services
    
    if [ "$open_browser_flag" = true ]; then
        open_browser
    else
        open_browser --no-browser
    fi
    
    show_info
    
    print_header "Startup completed successfully!"
}

# Error handling
trap 'print_error "Script interrupted"; exit 1' INT TERM

# Run main function with all arguments
main "$@"