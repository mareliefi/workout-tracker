#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════╗"
echo "║   🏋️  Workout Tracker Setup  🏋️      ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Load .env if exists
if [ -f .env ]; then
    echo -e "${GREEN}Loading environment variables from .env${NC}"
    export $(grep -v '^#' .env | xargs)
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not installed${NC}"
    exit 1
fi

# Determine docker-compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

echo -e "${BLUE}🛠️  Starting Development...${NC}"
$COMPOSE_CMD -f docker-compose.dev.yml up --build

echo -e "${GREEN}✅ Dev environment is running!${NC}"
echo "🌐 Open frontend at: http://localhost:3000"
echo "🖥️  Backend API at: http://localhost:5000"

