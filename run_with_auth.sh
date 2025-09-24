#!/bin/bash

# Reddit MCP Server with WorkOS Authentication
# Run this script to start the server with OAuth authentication enabled

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================"
echo "Reddit MCP Server with Auth"
echo "================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Creating .env from .env.sample..."
    cp .env.sample .env
    echo -e "${YELLOW}⚠️  Please edit .env and add your WorkOS credentials:${NC}"
    echo "   - WORKOS_CLIENT_ID"
    echo "   - WORKOS_CLIENT_SECRET"
    echo "   - WORKOS_AUTHKIT_DOMAIN"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Check for required WorkOS credentials
if [ -z "$WORKOS_CLIENT_ID" ] || [ -z "$WORKOS_CLIENT_SECRET" ] || [ -z "$WORKOS_AUTHKIT_DOMAIN" ]; then
    echo -e "${RED}❌ WorkOS credentials not configured!${NC}"
    echo ""
    echo "Please add the following to your .env file:"
    echo "  WORKOS_CLIENT_ID=client_YOUR_CLIENT_ID"
    echo "  WORKOS_CLIENT_SECRET=YOUR_SECRET"
    echo "  WORKOS_AUTHKIT_DOMAIN=https://your-app.authkit.app"
    echo ""
    echo "Get these from your WorkOS dashboard:"
    echo "  https://dashboard.workos.com"
    exit 1
fi

# Display configuration
echo -e "${GREEN}✅ WorkOS OAuth configured${NC}"
echo "   Domain: $WORKOS_AUTHKIT_DOMAIN"
echo "   Base URL: ${FASTMCP_SERVER_AUTH_WORKOS_BASE_URL:-http://localhost:8000}"
echo ""

# Set auth-specific environment variables
export FASTMCP_TRANSPORT=http
export FASTMCP_PORT=${FASTMCP_PORT:-8000}

# Check for Reddit credentials (optional but recommended)
if [ -z "$REDDIT_CLIENT_ID" ] || [ -z "$REDDIT_CLIENT_SECRET" ]; then
    echo -e "${YELLOW}⚠️  Reddit API credentials not configured${NC}"
    echo "   Server will run with limited functionality"
    echo "   Add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to .env for full features"
    echo ""
fi

echo "🚀 Starting server..."
echo "   Transport: http"
echo "   Port: $FASTMCP_PORT (if using HTTP)"
echo ""

# Run the server
if command -v python3 &> /dev/null; then
    python3 src/server.py
elif command -v python &> /dev/null; then
    python src/server.py
else
    echo -e "${RED}❌ Python not found!${NC}"
    echo "Please install Python 3.11 or higher"
    exit 1
fi