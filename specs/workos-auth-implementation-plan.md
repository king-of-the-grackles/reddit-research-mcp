# WorkOS Remote OAuth Implementation Plan for Reddit MCP

## Overview
Implement WorkOS AuthKit authentication for the Reddit MCP server using FastMCP's Remote OAuth pattern with Dynamic Client Registration (DCR). This provides enterprise-grade authentication with automatic client registration, using environment variables for all configuration.

## Implementation Status

✅ **All implementation tasks completed successfully!**

## Implementation Plan

### 1. Update Main Server with AuthKit Support ✅

**File**: `reddit-research-mcp/src/server.py`
**Status**: COMPLETED

Added AuthKitProvider import and conditional initialization based on environment variables:

```python
from fastmcp.server.auth.providers.workos import AuthKitProvider
import os

# Initialize auth provider from environment if configured
auth = None
if os.getenv('FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN'):
    auth = AuthKitProvider()  # Uses env vars automatically
    print(f"✓ AuthKit authentication enabled", flush=True)

mcp = FastMCP("Reddit MCP", auth=auth, instructions=...)
```

### 2. Create Environment Configuration Template ✅

**File**: `reddit-research-mcp/.env.sample`
**Status**: COMPLETED

```bash
# WorkOS AuthKit Configuration (Remote OAuth with DCR)
# Get these values from your WorkOS dashboard
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN=https://your-project.authkit.app
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL=https://your-server.com
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_REQUIRED_SCOPES=openid,profile,email

# Existing Reddit API configuration
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
```

### 3. Create Test Client ✅

**File**: `reddit-research-mcp/test_auth_client.py`
**Status**: COMPLETED

```python
from fastmcp import Client
import asyncio

async def test_authenticated_connection():
    """Test client that authenticates via WorkOS OAuth."""

    # The client will automatically:
    # 1. Discover auth requirements from the server
    # 2. Register with WorkOS via DCR
    # 3. Open browser for user authentication
    # 4. Store tokens for future requests

    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        print("✓ Authenticated successfully!")

        # Test an authenticated tool call
        result = await client.call_tool("discover_operations")
        print(f"Available operations: {result}")

        # Test fetching Reddit data
        subreddits = await client.call_tool(
            "execute_operation",
            {
                "operation_id": "discover_subreddits",
                "parameters": {"query": "python programming", "limit": 5}
            }
        )
        print(f"Found subreddits: {subreddits}")

if __name__ == "__main__":
    asyncio.run(test_authenticated_connection())
```

### 4. Update Dependencies ✅

**File**: `reddit-research-mcp/pyproject.toml`
**Status**: COMPLETED

Updated the FastMCP version to ensure AuthKitProvider support:

```toml
dependencies = [
    # ... existing dependencies ...
    "fastmcp>=2.12.0",  # Updated from 0.8.0 for AuthKit support
    # ... rest of dependencies ...
]
```

### 5. Create Setup Documentation ✅

**File**: `reddit-research-mcp/AUTH_SETUP.md`
**Status**: COMPLETED

```markdown
# WorkOS AuthKit Setup Guide

## Prerequisites

1. WorkOS account with an active project
2. Python 3.11+ environment
3. Reddit API credentials (existing)

## WorkOS Configuration

### Step 1: Enable AuthKit

1. Log in to [WorkOS Dashboard](https://dashboard.workos.com)
2. Navigate to your project
3. Go to **Authentication → AuthKit**
4. Enable AuthKit if not already enabled

### Step 2: Enable Dynamic Client Registration (DCR)

1. Go to **Applications → Configuration**
2. Toggle **Dynamic Client Registration** to enabled
3. This allows MCP clients to auto-register without manual configuration

### Step 3: Note Your AuthKit Domain

1. Find your AuthKit domain in the configuration
2. It looks like: `https://your-project-12345.authkit.app`
3. Save this for your `.env` file

## Server Configuration

### Step 1: Create `.env` file

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with your actual values
```

### Step 2: Install/Update Dependencies

```bash
uv sync  # or: pip install -e .
```

### Step 3: Run the Server

The server must run with HTTP transport for OAuth flows:

```bash
fastmcp run src/server.py --transport http --port 8000
```

## Testing Authentication

Run the test client:

```bash
python test_auth_client.py
```

On first run:
1. Browser opens to WorkOS login
2. User authenticates
3. Client receives token
4. Token cached for future requests

## Troubleshooting

### "DCR not enabled" error
- Enable Dynamic Client Registration in WorkOS dashboard

### "Invalid AuthKit domain"
- Verify domain format: `https://your-project.authkit.app`
- No trailing slash

### Token validation fails
- Check server logs for JWT verification errors
- Ensure AuthKit domain matches exactly
```

## How It Works

### Authentication Flow

1. **Server Startup**
   - Checks for `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN` env var
   - If present, initializes AuthKitProvider
   - Sets up OAuth discovery endpoints

2. **Client Discovery**
   - Client requests `/.well-known/oauth-protected-resource`
   - Server returns metadata pointing to WorkOS AuthKit

3. **Dynamic Client Registration**
   - Client registers itself with WorkOS automatically
   - Receives client credentials without manual setup

4. **User Authentication**
   - Client redirects to WorkOS login
   - User authenticates (SSO, username/password, etc.)
   - WorkOS issues JWT token

5. **Token Validation**
   - Client includes token in MCP requests
   - Server validates JWT using WorkOS public keys
   - Extracts user information from token claims

### Key Components

#### AuthKitProvider (RemoteAuthProvider)
- Provides OAuth discovery metadata
- Configures JWT verification
- Forwards authorization server metadata
- Validates redirect URIs

#### Token Verification
- Uses JWTVerifier with WorkOS JWKS endpoint
- Validates token signature and expiration
- Checks required scopes
- Extracts user claims

#### Environment Variables
- `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN`: WorkOS AuthKit URL
- `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL`: Your server's public URL
- `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_REQUIRED_SCOPES`: OAuth scopes to require

## Benefits

### Security
- Enterprise-grade authentication via WorkOS
- JWT tokens with cryptographic signatures
- Automatic token expiration and rotation
- Scope-based access control

### Developer Experience
- Zero client configuration with DCR
- Automatic OAuth flow handling
- Built-in token caching
- Clean separation of auth and business logic

### Production Ready
- Environment-based configuration
- Comprehensive error handling
- Logging and monitoring support
- Scalable architecture

## Next Steps

1. Set up WorkOS account and enable AuthKit
2. Configure environment variables
3. Update server.py with auth support
4. Test with authenticated client
5. Deploy to production with HTTPS

## Notes

- Server must run with HTTP/HTTPS transport (not stdio) for OAuth flows
- DCR eliminates need for manual client registration
- Tokens are automatically refreshed by MCP clients
- All auth logic handled by FastMCP and WorkOS