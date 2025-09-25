#!/usr/bin/env python3
"""
OAuth Flow Testing Script for Reddit MCP Server
Tests the OAuth token lifecycle and debugging
"""

import asyncio
import json
import sys
import time
from datetime import datetime, timedelta
import httpx
import jwt
import os
from typing import Optional, Dict, Any

# Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://reddit-research-mcp.fastmcp.app/mcp")
DEBUG_URL = os.getenv("DEBUG_URL", "https://reddit-research-mcp.fastmcp.app/debug/auth")


class OAuthFlowTester:
    """Test OAuth flow and token lifecycle."""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.token: Optional[str] = None
        self.token_data: Optional[Dict[str, Any]] = None
        self.test_results = []

    async def test_debug_endpoint(self):
        """Test the debug endpoint without auth."""
        print("\n=== Testing Debug Endpoint (No Auth) ===")
        try:
            response = await self.client.get(DEBUG_URL)
            if response.status_code == 200:
                data = response.json()
                print(f"Debug Info: {json.dumps(data, indent=2)}")
                self.test_results.append(("debug_endpoint_noauth", "PASS", data))
            else:
                print(f"Debug endpoint failed: {response.status_code}")
                self.test_results.append(("debug_endpoint_noauth", "FAIL", response.status_code))
        except Exception as e:
            print(f"Error accessing debug endpoint: {e}")
            self.test_results.append(("debug_endpoint_noauth", "ERROR", str(e)))

    async def test_auth_discovery(self):
        """Test OAuth authorization server discovery."""
        print("\n=== Testing OAuth Discovery ===")
        discovery_url = MCP_SERVER_URL.replace("/mcp", "/.well-known/oauth-authorization-server")

        try:
            response = await self.client.get(discovery_url)
            if response.status_code == 200:
                data = response.json()
                print(f"Authorization Server: {data.get('issuer', 'unknown')}")
                print(f"Token Endpoint: {data.get('token_endpoint', 'unknown')}")
                print(f"Auth Endpoint: {data.get('authorization_endpoint', 'unknown')}")
                self.test_results.append(("oauth_discovery", "PASS", data))
                return data
            else:
                print(f"Discovery failed: {response.status_code}")
                self.test_results.append(("oauth_discovery", "FAIL", response.status_code))
        except Exception as e:
            print(f"Error in OAuth discovery: {e}")
            self.test_results.append(("oauth_discovery", "ERROR", str(e)))

        return None

    async def test_initial_connection(self):
        """Test initial MCP connection without auth."""
        print("\n=== Testing Initial Connection ===")
        try:
            # Try to connect without auth (should fail with 401)
            response = await self.client.post(
                MCP_SERVER_URL,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "clientInfo": {
                            "name": "OAuth Test Client",
                            "version": "1.0.0"
                        }
                    }
                }
            )

            print(f"Response Status: {response.status_code}")
            if response.status_code == 401:
                print("Expected 401 Unauthorized - Auth is required")
                self.test_results.append(("initial_connection", "PASS", "401 as expected"))
            else:
                print(f"Unexpected response: {response.text[:200]}")
                self.test_results.append(("initial_connection", "UNEXPECTED", response.status_code))
        except Exception as e:
            print(f"Connection error: {e}")
            self.test_results.append(("initial_connection", "ERROR", str(e)))

    async def simulate_token_lifecycle(self):
        """Simulate token usage over time to detect expiration issues."""
        print("\n=== Simulating Token Lifecycle ===")

        # Mock a bearer token for testing (in production, this would come from OAuth flow)
        # Note: This is just for testing token validation, not actual auth
        test_token = self.generate_test_token()

        print(f"Testing with mock token (first 50 chars): {test_token[:50]}...")

        # Test with token at different time intervals
        for i in range(3):
            print(f"\n--- Request {i+1} ---")
            headers = {"Authorization": f"Bearer {test_token}"}

            try:
                # Test debug endpoint with token
                response = await self.client.get(DEBUG_URL, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    print(f"Token accepted - TTL remaining: {data.get('token_ttl_remaining', 'unknown')}s")
                    print(f"Token expired: {data.get('token_expired', 'unknown')}")
                else:
                    print(f"Token rejected: {response.status_code}")

                # Test MCP endpoint with token
                mcp_response = await self.client.post(
                    MCP_SERVER_URL,
                    headers=headers,
                    json={
                        "jsonrpc": "2.0",
                        "id": i+1,
                        "method": "tools/list",
                        "params": {}
                    }
                )
                print(f"MCP Response: {mcp_response.status_code}")

            except Exception as e:
                print(f"Request error: {e}")

            # Wait before next request
            if i < 2:
                print(f"Waiting 5 seconds before next request...")
                await asyncio.sleep(5)

    def generate_test_token(self) -> str:
        """Generate a test JWT token for debugging purposes."""
        # This creates a mock token for testing - in production this comes from OAuth
        now = time.time()
        payload = {
            "sub": "user_01K5WR6Z4XTBN53M4TEJWWEEN17",  # Match the client ID from logs
            "exp": int(now + 300),  # 5 minutes from now
            "iat": int(now),
            "scope": "read write",
            "iss": "https://fascinating-forest-70.authkit.app",
            "client_id": "client_test_123"
        }
        # Note: This uses 'none' algorithm for testing only
        # Real tokens must be properly signed
        return jwt.encode(payload, "", algorithm="none")

    async def run_all_tests(self):
        """Run all OAuth flow tests."""
        print("=" * 60)
        print("Starting OAuth Flow Tests")
        print(f"Server: {MCP_SERVER_URL}")
        print(f"Time: {datetime.now().isoformat()}")
        print("=" * 60)

        # Run tests
        await self.test_debug_endpoint()
        discovery = await self.test_auth_discovery()
        await self.test_initial_connection()
        await self.simulate_token_lifecycle()

        # Print summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        for test_name, status, details in self.test_results:
            print(f"{test_name:30} {status:10}")

        # Save detailed results
        results_file = f"oauth_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "server": MCP_SERVER_URL,
                "results": self.test_results
            }, f, indent=2, default=str)
        print(f"\nDetailed results saved to: {results_file}")

    async def close(self):
        """Clean up resources."""
        await self.client.aclose()


async def main():
    """Main test runner."""
    tester = OAuthFlowTester()
    try:
        await tester.run_all_tests()
    finally:
        await tester.close()


if __name__ == "__main__":
    # Enable debug output
    if "--debug" in sys.argv:
        os.environ["FASTMCP_DEBUG_TOKENS"] = "true"
        print("Token debugging enabled")

    asyncio.run(main())