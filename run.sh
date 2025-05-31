#!/bin/bash

# Enhanced Agentic AI Server - Run Script
# This script helps you easily run the server in different modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "🤖 Enhanced Agentic AI Server"
    echo "========================================"
    echo -e "${NC}"
}

print_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev         Run in development mode"
    echo "  prod        Run in production mode"
    echo "  docker      Run with Docker"
    echo "  compose     Run with Docker Compose"
    echo "  test        Run test client"
    echo "  setup       Setup environment"
    echo "  clean       Clean temporary files"
    echo "  help        Show this help message"
}

setup_environment() {
    echo -e "${YELLOW}Setting up environment...${NC}"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo -e "${BLUE}Creating .env file from template...${NC}"
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env file with your configurations${NC}"
    fi
    
    # Create data directory
    mkdir -p data
    
    # Install Python dependencies
    echo -e "${BLUE}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    
    echo -e "${GREEN}✅ Environment setup complete!${NC}"
}

run_development() {
    echo -e "${YELLOW}Starting development server...${NC}"
    export FLASK_DEBUG=True
    export FLASK_ENV=development
    python app.py
}

run_production() {
    echo -e "${YELLOW}Starting production server...${NC}"
    export FLASK_DEBUG=False
    export FLASK_ENV=production
    gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
}

run_docker() {
    echo -e "${YELLOW}Building and running with Docker...${NC}"
    
    # Build Docker image
    echo -e "${BLUE}Building Docker image...${NC}"
    docker build -t agentic-ai-server .
    
    # Run Docker container
    echo -e "${BLUE}Running Docker container...${NC}"
    docker run -p 5000:5000 \
        --name agentic-ai-server \
        -v $(pwd)/data:/app/data \
        -v /var/run/docker.sock:/var/run/docker.sock \
        --rm \
        agentic-ai-server
}

run_compose() {
    echo -e "${YELLOW}Starting with Docker Compose...${NC}"
    docker-compose up --build
}

run_test() {
    echo -e "${YELLOW}Running test client...${NC}"
    python test_client.py
}

clean_files() {
    echo -e "${YELLOW}Cleaning temporary files...${NC}"
    
    # Remove Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove logs
    rm -f *.log
    
    # Remove Docker containers and images (optional)
    read -p "Remove Docker containers and images? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker container prune -f
        docker image prune -f
    fi
    
    echo -e "${GREEN}✅ Cleanup complete!${NC}"
}

check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}⚠️  Docker is not installed (required for code execution)${NC}"
    fi
    
    # Check pip
    if ! command -v pip &> /dev/null; then
        echo -e "${RED}❌ pip is not installed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Dependencies check passed${NC}"
}

# Main script logic
print_banner

case "${1:-help}" in
    "dev")
        check_dependencies
        run_development
        ;;
    "prod")
        check_dependencies
        run_production
        ;;
    "docker")
        run_docker
        ;;
    "compose")
        run_compose
        ;;
    "test")
        run_test
        ;;
    "setup")
        setup_environment
        ;;
    "clean")
        clean_files
        ;;
    "help"|*)
        print_help
        ;;
esac