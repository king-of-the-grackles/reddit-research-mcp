#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastmcp>=0.8.0",
#     "langfuse>=2.50.0",
#     "python-dotenv>=1.0.0",
#     "praw>=7.7.1",
# ]
# ///

"""Test script to verify Langfuse observability is working."""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_langfuse_config():
    """Test Langfuse configuration."""
    print("Testing Langfuse configuration...")
    
    from src.config import get_langfuse_client
    
    client = get_langfuse_client()
    
    if client is None:
        print("❌ Langfuse client not configured")
        print("   Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY to enable observability")
        return False
    
    print("✅ Langfuse client initialized")
    
    # Try to verify connection if enabled
    if os.environ.get("LANGFUSE_VERIFY_CONNECTION", "false").lower() == "true":
        try:
            if client.auth_check():
                print("✅ Langfuse connection verified")
            else:
                print("❌ Langfuse authentication failed")
                return False
        except Exception as e:
            print(f"❌ Langfuse connection error: {e}")
            return False
    else:
        print("ℹ️  Set LANGFUSE_VERIFY_CONNECTION=true to test connection")
    
    return True

def test_middleware_integration():
    """Test middleware integration with FastMCP."""
    print("\nTesting middleware integration...")
    
    from fastmcp import FastMCP
    from src.middleware.langfuse_middleware import LangfuseMiddleware
    from src.config import get_langfuse_client
    
    # Create test server
    mcp = FastMCP("Test Server")
    
    # Try to add middleware
    client = get_langfuse_client()
    if client:
        middleware = LangfuseMiddleware(client)
        mcp.add_middleware(middleware)
        print("✅ Middleware added to FastMCP server")
        return True
    else:
        print("⚠️  Middleware not added (Langfuse not configured)")
        return False

def test_trace_generation():
    """Test trace ID generation."""
    print("\nTesting trace ID generation...")
    
    from src.middleware.langfuse_middleware import LangfuseMiddleware
    from unittest.mock import Mock
    
    # Create mock client
    mock_client = Mock()
    middleware = LangfuseMiddleware(mock_client)
    
    # Generate trace ID
    trace_id = middleware._ensure_w3c_trace_id()
    
    # Verify W3C format (32 hex chars)
    if len(trace_id) == 32 and all(c in '0123456789abcdef' for c in trace_id):
        print(f"✅ W3C-compliant trace ID generated: {trace_id}")
        return True
    else:
        print(f"❌ Invalid trace ID format: {trace_id}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Langfuse Observability Test")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(test_langfuse_config())
    results.append(test_middleware_integration())
    results.append(test_trace_generation())
    
    # Summary
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {sum(results)}/{len(results)} tests passed")
    print("=" * 50)

if __name__ == "__main__":
    main()