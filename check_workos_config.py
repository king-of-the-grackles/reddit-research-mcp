#!/usr/bin/env python3
"""
WorkOS Configuration Checker
Verifies WorkOS AuthKit settings and token configuration
"""

import os
import sys
import json
from datetime import datetime
import httpx
import asyncio
from typing import Dict, Any, Optional


class WorkOSConfigChecker:
    """Check WorkOS AuthKit configuration and token settings."""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.config = {
            "authkit_domain": os.getenv("WORKOS_AUTHKIT_DOMAIN", os.getenv("FASTMCP_SERVER_AUTH_WORKOS_AUTHKIT_DOMAIN")),
            "client_id": os.getenv("WORKOS_CLIENT_ID", os.getenv("FASTMCP_SERVER_AUTH_WORKOS_CLIENT_ID")),
            "client_secret": os.getenv("WORKOS_CLIENT_SECRET", os.getenv("FASTMCP_SERVER_AUTH_WORKOS_CLIENT_SECRET")),
            "base_url": os.getenv("FASTMCP_SERVER_AUTH_WORKOS_BASE_URL", "https://reddit-research-mcp.fastmcp.app"),
            "callback_path": os.getenv("FASTMCP_SERVER_AUTH_WORKOS_CALLBACK_PATH", "/auth/callback"),
        }
        self.issues = []
        self.recommendations = []

    def check_environment_vars(self):
        """Check if required environment variables are set."""
        print("\n=== Environment Variables ===")

        for key, value in self.config.items():
            if key == "client_secret" and value:
                # Mask the secret
                display_value = f"***{value[-4:]}" if len(value) > 4 else "***"
            else:
                display_value = value or "NOT SET"

            status = "✓" if value else "✗"
            print(f"{status} {key:20} = {display_value}")

            if not value and key != "client_secret":
                self.issues.append(f"{key} is not set")

        # Check for mode settings
        auth_mode = os.getenv("FASTMCP_SERVER_AUTH_WORKOS_MODE", "auto")
        print(f"  AUTH_MODE           = {auth_mode}")

    async def check_authkit_discovery(self):
        """Check if AuthKit domain is accessible and properly configured."""
        print("\n=== AuthKit Discovery ===")

        if not self.config["authkit_domain"]:
            print("✗ No AuthKit domain configured")
            self.issues.append("AuthKit domain not configured")
            return None

        # Clean up domain
        domain = self.config["authkit_domain"].strip().rstrip("/")
        if not domain.startswith("http"):
            domain = f"https://{domain}"

        discovery_url = f"{domain}/.well-known/openid-configuration"
        print(f"Checking: {discovery_url}")

        try:
            response = await self.client.get(discovery_url)
            if response.status_code == 200:
                data = response.json()
                print("✓ AuthKit discovery successful")
                print(f"  Issuer: {data.get('issuer', 'unknown')}")
                print(f"  Token Endpoint: {data.get('token_endpoint', 'unknown')}")
                print(f"  Auth Endpoint: {data.get('authorization_endpoint', 'unknown')}")

                # Check token expiration settings
                if "token_endpoint_auth_methods_supported" in data:
                    print(f"  Auth Methods: {', '.join(data['token_endpoint_auth_methods_supported'])}")

                return data
            else:
                print(f"✗ Discovery failed: HTTP {response.status_code}")
                self.issues.append(f"AuthKit discovery returned {response.status_code}")
        except Exception as e:
            print(f"✗ Discovery error: {e}")
            self.issues.append(f"AuthKit discovery failed: {str(e)}")

        return None

    async def check_token_settings(self, discovery_data: Optional[Dict[str, Any]]):
        """Analyze token configuration from discovery data."""
        print("\n=== Token Configuration Analysis ===")

        if not discovery_data:
            print("⚠ No discovery data available")
            return

        # Common token lifetime issues
        print("\nToken Lifetime Recommendations:")
        print("1. Access tokens should have at least 15 minutes TTL for MCP operations")
        print("2. Refresh tokens should be enabled for long-running sessions")
        print("3. Consider using sliding expiration for active sessions")

        # Check if the server supports refresh tokens
        if "grant_types_supported" in discovery_data:
            grants = discovery_data["grant_types_supported"]
            has_refresh = "refresh_token" in grants
            print(f"\n{'✓' if has_refresh else '✗'} Refresh token support: {has_refresh}")
            if not has_refresh:
                self.issues.append("Refresh tokens not supported")
                self.recommendations.append("Enable refresh_token grant type in WorkOS")

    def check_callback_configuration(self):
        """Verify callback URL configuration."""
        print("\n=== Callback Configuration ===")

        base_url = self.config["base_url"]
        callback_path = self.config["callback_path"]

        if base_url and callback_path:
            callback_url = f"{base_url.rstrip('/')}{callback_path}"
            print(f"✓ Callback URL: {callback_url}")
            print("\nMake sure this URL is registered in WorkOS dashboard:")
            print("1. Go to WorkOS Dashboard > AuthKit > Redirects")
            print(f"2. Add: {callback_url}")
            print("3. Save changes")
        else:
            print("✗ Cannot determine callback URL")
            self.issues.append("Callback URL cannot be determined")

    def analyze_common_issues(self):
        """Analyze common OAuth/MCP integration issues."""
        print("\n=== Common Issues Analysis ===")

        # Check for token expiration issues
        print("\n1. Token Expiration Issues:")
        print("   - Symptom: Initial auth works, subsequent requests fail")
        print("   - Solution: Increase token TTL in WorkOS to at least 15 minutes")
        self.recommendations.append("Configure longer token TTL in WorkOS (min 15 minutes)")

        # Check for client ID mismatch
        print("\n2. Client ID Consistency:")
        print("   - Symptom: 'Bearer token rejected for client' errors")
        print("   - Solution: Ensure mcp-remote maintains same client session")
        self.recommendations.append("Verify mcp-remote is not creating new sessions per request")

        # Check for scope issues
        print("\n3. Scope Configuration:")
        print("   - Current scopes: Not set (defaults to basic)")
        print("   - Recommended: Set explicit scopes if required by your MCP tools")

        # Server restart issues
        print("\n4. Server Process Cycling:")
        print("   - Symptom: Server PIDs changing frequently in logs")
        print("   - Solution: Check if FastMCP is restarting on auth failures")
        self.recommendations.append("Monitor server stability - frequent restarts break OAuth sessions")

    def generate_fix_script(self):
        """Generate a script to fix common issues."""
        print("\n=== Generating Fix Recommendations ===")

        script_content = """#!/bin/bash
# WorkOS Configuration Fix Script
# Generated: {timestamp}

echo "Setting up WorkOS configuration for Reddit MCP..."

# 1. Set required environment variables
export WORKOS_AUTHKIT_DOMAIN="{authkit_domain}"
export WORKOS_CLIENT_ID="{client_id}"
export WORKOS_CLIENT_SECRET="<YOUR_SECRET_HERE>"
export FASTMCP_SERVER_AUTH_WORKOS_BASE_URL="{base_url}"
export FASTMCP_SERVER_AUTH_WORKOS_MODE="authkit"

# 2. Enable debug logging
export FASTMCP_LOG_LEVEL="DEBUG"
export FASTMCP_WORKOS_DEBUG="true"
export FASTMCP_DEBUG_TOKENS="true"

# 3. Test with extended token lifetime (for debugging)
# Note: This must be configured in WorkOS Dashboard
echo "Remember to configure in WorkOS Dashboard:"
echo "  - Token TTL: 3600 seconds (1 hour)"
echo "  - Enable refresh tokens"
echo "  - Add callback URL: {callback_url}"

# 4. Test connection
echo "Testing MCP connection..."
codex mcp list

echo "Check logs for token validation details"
""".format(
            timestamp=datetime.now().isoformat(),
            authkit_domain=self.config["authkit_domain"] or "<YOUR_AUTHKIT_DOMAIN>",
            client_id=self.config["client_id"] or "<YOUR_CLIENT_ID>",
            base_url=self.config["base_url"],
            callback_url=f"{self.config['base_url'].rstrip('/')}{self.config['callback_path']}"
        )

        fix_file = "fix_workos_config.sh"
        with open(fix_file, "w") as f:
            f.write(script_content)
        os.chmod(fix_file, 0o755)
        print(f"✓ Fix script saved to: {fix_file}")

    async def run_checks(self):
        """Run all configuration checks."""
        print("=" * 60)
        print("WorkOS Configuration Checker")
        print(f"Time: {datetime.now().isoformat()}")
        print("=" * 60)

        # Run checks
        self.check_environment_vars()
        discovery = await self.check_authkit_discovery()
        await self.check_token_settings(discovery)
        self.check_callback_configuration()
        self.analyze_common_issues()
        self.generate_fix_script()

        # Print summary
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)

        if self.issues:
            print("\n❌ Issues Found:")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("\n✓ No critical issues found")

        if self.recommendations:
            print("\n💡 Recommendations:")
            for rec in self.recommendations:
                print(f"  - {rec}")

        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "config": {k: v if k != "client_secret" else "***" for k, v in self.config.items()},
            "issues": self.issues,
            "recommendations": self.recommendations,
            "discovery_data": discovery
        }

        report_file = f"workos_config_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n📄 Full report saved to: {report_file}")

    async def close(self):
        """Clean up resources."""
        await self.client.aclose()


async def main():
    """Main checker."""
    checker = WorkOSConfigChecker()
    try:
        await checker.run_checks()
    finally:
        await checker.close()


if __name__ == "__main__":
    asyncio.run(main())