#!/bin/bash
#
# Run Critical Pre-Production Tests for Reddit MCP Server
# This script runs all critical tests to ensure the server is ready for production
#

set -e  # Exit on first error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo "============================================================"
echo "🚀 REDDIT MCP SERVER - PRE-PRODUCTION TEST SUITE"
echo "============================================================"
echo ""

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1)
echo "  Using: $python_version"

# Check if running from correct directory
if [ ! -f "src/server.py" ]; then
    echo -e "${RED}❌ ERROR: Must run from project root directory${NC}"
    echo "  Please cd to reddit-mcp-poc directory and run again"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import fastmcp" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install -e ".[dev]" --quiet
fi

# Track test results
all_passed=true
test_results=()

# Function to run a test and track results
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo ""
    echo -e "${BLUE}Running: $test_name${NC}"
    echo "------------------------------------------------------------"
    
    if $test_command; then
        test_results+=("✅ $test_name: PASSED")
    else
        test_results+=("❌ $test_name: FAILED")
        all_passed=false
    fi
}

# 1. Core MCP Functionality Test
run_test "Core MCP Functionality" "python3 tests/test_mcp_critical.py"

# 2. Langfuse Observability Test  
run_test "Langfuse Observability" "python3 tests/test_langfuse_critical.py"

# 3. Security Tests
run_test "Security Checks" "python3 tests/test_security_critical.py"

# 4. End-to-End Smoke Test
run_test "End-to-End Workflow" "python3 tests/test_e2e_smoke.py"

# 5. Quick existing tests
echo ""
echo -e "${BLUE}Running existing test scripts...${NC}"
echo "------------------------------------------------------------"

if [ -f "scripts/test_observability.py" ]; then
    run_test "Observability Script" "python3 scripts/test_observability.py"
fi

if [ -f "scripts/test_operations_tracking.py" ]; then
    # Set test credentials for this test
    export LANGFUSE_PUBLIC_KEY="pk-lf-fb913137-015d-4d05-970b-1915a2ef13b8"
    export LANGFUSE_SECRET_KEY="sk-lf-9bd1ea11-d794-432b-a04f-e043636eb7cc"
    export LANGFUSE_HOST="https://us.cloud.langfuse.com"
    export REDDIT_CLIENT_ID="test_id"
    export REDDIT_CLIENT_SECRET="test_secret"
    
    run_test "Operations Tracking" "python3 scripts/test_operations_tracking.py"
    
    # Clean up test credentials
    unset LANGFUSE_PUBLIC_KEY
    unset LANGFUSE_SECRET_KEY
    unset LANGFUSE_HOST
    unset REDDIT_CLIENT_ID
    unset REDDIT_CLIENT_SECRET
fi

# Unit tests section removed - test_tools.py was outdated and deleted

# Summary
echo ""
echo "============================================================"
echo "📊 TEST RESULTS SUMMARY"
echo "============================================================"
echo ""

for result in "${test_results[@]}"; do
    echo "  $result"
done

echo ""
echo "------------------------------------------------------------"

if [ "$all_passed" = true ]; then
    echo -e "${GREEN}✅ ALL CRITICAL TESTS PASSED!${NC}"
    echo ""
    echo "🎉 Server is ready for production deployment!"
    echo ""
    echo "Next steps:"
    echo "  1. Set production environment variables:"
    echo "     - REDDIT_CLIENT_ID"
    echo "     - REDDIT_CLIENT_SECRET"
    echo "     - LANGFUSE_PUBLIC_KEY (optional)"
    echo "     - LANGFUSE_SECRET_KEY (optional)"
    echo ""
    echo "  2. Test with real MCP client:"
    echo "     - Claude Desktop or MCP Inspector"
    echo ""
    echo "  3. Check Langfuse dashboard for traces:"
    echo "     - https://us.cloud.langfuse.com"
    echo ""
    echo "  4. Deploy to production! 🚀"
else
    echo -e "${RED}❌ SOME TESTS FAILED!${NC}"
    echo ""
    echo "Please fix the issues above before deploying to production."
    echo ""
    echo "Debug tips:"
    echo "  1. Check individual test output above"
    echo "  2. Review error messages and stack traces"
    echo "  3. Ensure all dependencies are installed"
    echo "  4. Verify environment variables are set correctly"
    exit 1
fi

echo "============================================================"