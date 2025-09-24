#!/bin/bash

# Reddit MCP Server - Local Development Mode
# Run this script to start the server WITHOUT authentication (stdio transport)

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================"
echo "Reddit MCP Server (Dev Mode)"
echo "================================"

# Check if .env file exists for Reddit credentials
if [ -f .env ]; then
    # Load only Reddit-related environment variables
    export $(grep -E '^REDDIT_|^CHROMA_' .env | grep -v '^#' | xargs)
    echo -e "${GREEN}✅ Environment variables loaded${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "   Server will run with limited functionality"
fi

# Explicitly unset WorkOS variables to ensure auth is disabled
unset WORKOS_CLIENT_ID
unset WORKOS_CLIENT_SECRET
unset WORKOS_AUTHKIT_DOMAIN
unset FASTMCP_SERVER_AUTH_WORKOS_CLIENT_ID
unset FASTMCP_SERVER_AUTH_WORKOS_CLIENT_SECRET
unset FASTMCP_SERVER_AUTH_WORKOS_AUTHKIT_DOMAIN
unset FASTMCP_SERVER_AUTH_WORKOS_BASE_URL
unset FASTMCP_SERVER_AUTH

# Set transport to stdio for local development
export FASTMCP_TRANSPORT=stdio

# Check for Reddit credentials
if [ -z "$REDDIT_CLIENT_ID" ] || [ -z "$REDDIT_CLIENT_SECRET" ]; then
    echo -e "${YELLOW}⚠️  Reddit API credentials not configured${NC}"
    echo "   Server will run with limited functionality"
    echo "   Add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to .env for full features"
fi

echo ""
echo "🚀 Starting server..."
echo "   Transport: stdio (no authentication)"
echo "   Mode: Development"
echo ""
echo "This mode is for local development only."
echo "For production with auth, use: ./run_with_auth.sh"
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