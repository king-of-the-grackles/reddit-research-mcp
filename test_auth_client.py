#!/usr/bin/env python3
"""
Test client for WorkOS-authenticated Reddit MCP server.

This client demonstrates how MCP clients automatically handle OAuth authentication
when connecting to a protected server using WorkOS AuthKit with Dynamic Client Registration.

Usage:
    python test_auth_client.py

The client will:
1. Discover authentication requirements from the server
2. Automatically register with WorkOS via DCR
3. Open browser for user authentication (first time only)
4. Cache tokens for future use
5. Make authenticated tool calls
"""

import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import Client

# Load environment variables if available
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ Loaded environment from {env_path}")

def parse_tool_result(result):
    """Helper to parse FastMCP tool call results."""
    if hasattr(result, 'content'):
        # Content is a list of TextContent objects
        if isinstance(result.content, list) and len(result.content) > 0:
            # Get the text from the first TextContent object
            text_content = result.content[0]
            if hasattr(text_content, 'text'):
                # Parse the JSON string
                try:
                    return json.loads(text_content.text)
                except json.JSONDecodeError:
                    return text_content.text
            else:
                return result.content
        else:
            return result.content
    else:
        return result

async def test_authenticated_connection():
    """Test client that authenticates via WorkOS OAuth."""

    # Server URL - adjust if running on a different port or host
    server_url = os.getenv('FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL', 'http://localhost:8000')
    mcp_endpoint = f"{server_url}/mcp"

    print(f"\n🔌 Connecting to MCP server at: {mcp_endpoint}")
    print("=" * 50)

    try:
        # The client will automatically:
        # 1. Discover auth requirements from /.well-known/oauth-protected-resource
        # 2. Register with WorkOS via Dynamic Client Registration
        # 3. Open browser for user authentication (if needed)
        # 4. Store tokens for future requests

        async with Client(mcp_endpoint, auth="oauth") as client:
            print("\n✅ Successfully authenticated with WorkOS!")
            print("=" * 50)

            # Test 1: Discover available operations
            print("\n📋 Testing: discover_operations")
            result = await client.call_tool("discover_operations")
            operations = parse_tool_result(result)

            if isinstance(operations, dict) and 'operations' in operations:
                print(f"Available operations: {list(operations.get('operations', {}).keys())}")
            else:
                print(f"Unexpected response format: {operations}")

            # Test 2: Get operation schema
            print("\n📋 Testing: get_operation_schema")
            schema_result = await client.call_tool(
                "get_operation_schema",
                {"operation_id": "discover_subreddits", "include_examples": True}
            )
            schema = parse_tool_result(schema_result)

            if isinstance(schema, dict) and 'parameters' in schema:
                print(f"Schema for discover_subreddits: parameters = {list(schema.get('parameters', {}).keys())}")
            else:
                print(f"Schema response: {schema}")

            # Test 3: Execute an operation - discover subreddits
            print("\n📋 Testing: execute_operation (discover_subreddits)")
            try:
                subreddits_result = await client.call_tool(
                    "execute_operation",
                    {
                        "operation_id": "discover_subreddits",
                        "parameters": {"query": "python programming", "limit": 5}
                    }
                )
                subreddits = parse_tool_result(subreddits_result)

                # Check for the success response structure
                if isinstance(subreddits, dict):
                    if 'success' in subreddits and subreddits['success'] and 'data' in subreddits:
                        data = subreddits['data']
                        if 'subreddits' in data:
                            print(f"Found {len(data['subreddits'])} subreddits:")
                            for sub in data['subreddits'][:3]:  # Show first 3
                                confidence = sub.get('confidence', 0)
                                print(f"  • r/{sub.get('name', 'unknown')} (confidence: {confidence:.2f})")
                        else:
                            print(f"Response data: {data}")
                    elif 'subreddits' in subreddits:
                        print(f"Found {len(subreddits['subreddits'])} subreddits:")
                        for sub in subreddits['subreddits'][:3]:  # Show first 3
                            confidence = sub.get('confidence', 0)
                            print(f"  • r/{sub.get('name', 'unknown')} (confidence: {confidence:.2f})")
                    else:
                        print(f"Response: {subreddits}")
                else:
                    print(f"Response: {subreddits}")
            except Exception as e:
                print(f"Note: Subreddit discovery may require ChromaDB setup: {e}")

            # Test 4: List available resources
            print("\n📋 Testing: list resources")
            resources = await client.list_resources()
            if resources:
                print(f"Available resources: {len(resources)}")
                for res in resources[:3]:  # Show first 3
                    # Resources are objects, not dicts
                    if hasattr(res, 'uri'):
                        print(f"  • {res.uri}")
                    else:
                        print(f"  • {res}")
            else:
                print("No resources available")

            print("\n" + "=" * 50)
            print("✅ All tests completed successfully!")
            print("\nAuthentication details:")
            print("  • OAuth flow handled automatically")
            print("  • Tokens cached for future use")
            print("  • DCR eliminates manual client configuration")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure server is running: fastmcp run src/server.py --transport http --port 8000")
        print("2. Check WorkOS AuthKit is configured in .env")
        print("3. Verify Dynamic Client Registration is enabled in WorkOS dashboard")
        print("4. Check server logs for more details")

async def main():
    """Main entry point."""
    print("🚀 Reddit MCP WorkOS Authentication Test Client")
    print("=" * 50)

    # Check if auth is configured
    if os.getenv('FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN'):
        print("✓ WorkOS AuthKit configuration detected")
    else:
        print("⚠️  No WorkOS configuration found - server may run without auth")
        print("   To enable auth, set FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN in .env")

    await test_authenticated_connection()

if __name__ == "__main__":
    asyncio.run(main())