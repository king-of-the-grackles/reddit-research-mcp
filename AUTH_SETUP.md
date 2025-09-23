# WorkOS AuthKit Setup Guide for Reddit MCP

This guide walks you through setting up WorkOS AuthKit authentication for the Reddit MCP server. AuthKit provides enterprise-grade authentication with Dynamic Client Registration (DCR), allowing MCP clients to authenticate automatically without manual configuration.

## Prerequisites

- Python 3.11+ environment
- Reddit API credentials (existing setup)
- WorkOS account (free tier available)

## Quick Start

### 1. WorkOS Dashboard Configuration

#### Create WorkOS Account
1. Sign up at [WorkOS Dashboard](https://dashboard.workos.com)
2. Create a new project or use an existing one

#### Enable AuthKit
1. Navigate to **Authentication → AuthKit**
2. Enable AuthKit if not already enabled
3. Note your **AuthKit Domain** (e.g., `https://your-project-12345.authkit.app`)

#### Enable Dynamic Client Registration (Critical!)
1. Go to **Applications → Configuration**
2. Toggle **Dynamic Client Registration** to **Enabled**
3. This allows MCP clients to auto-register without manual configuration

![Enable DCR](https://workos.com/docs/images/dcr-enable.png)

### 2. Server Configuration

#### Set Environment Variables

1. Copy the sample environment file:
```bash
cp .env.sample .env
```

2. Edit `.env` with your WorkOS configuration:
```bash
# Required for authentication
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN=https://handsome-edge-83-staging.authkit.app
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL=http://localhost:8000
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_REQUIRED_SCOPES=openid,profile,email

# Your existing Reddit API credentials
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
```

#### Install/Update Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -e .
```

The server requires `fastmcp>=2.12.0` for AuthKit support.

### 3. Running the Server

The server MUST run with HTTP transport for OAuth flows:

```bash
# Using FastMCP CLI
fastmcp run src/server.py --transport http --port 8000

# Or directly with Python
cd src && python -m uvicorn server:app --port 8000
```

You should see:
```
✓ AuthKit authentication enabled
INFO:     Started server process
INFO:     Uvicorn running on http://localhost:8000
```

### 4. Testing Authentication

Run the included test client:

```bash
python test_auth_client.py
```

**First Run Experience:**
1. Client discovers auth requirements from server
2. Automatically registers with WorkOS via DCR
3. Browser opens for authentication
4. User logs in (or SSO if configured)
5. Client receives and caches token
6. Authenticated requests succeed

**Subsequent Runs:**
- Cached tokens are used automatically
- No browser interaction needed
- Tokens refresh automatically

## Configuration Options

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN` | Yes | Your WorkOS AuthKit domain | `https://project.authkit.app` |
| `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL` | Yes | Your server's public URL | `http://localhost:8000` |
| `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_REQUIRED_SCOPES` | No | OAuth scopes to require | `openid,profile,email` |

### OAuth Scopes

Common scopes for MCP servers:
- `openid` - Basic OpenID Connect
- `profile` - User profile information
- `email` - User email address
- `offline_access` - Refresh tokens for long-lived sessions

## How It Works

### Architecture

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│  MCP Client │◀─────▶│  MCP Server  │◀─────▶│   WorkOS    │
└─────────────┘       └──────────────┘       └─────────────┘
      │                      │                      │
      │ 1. Request           │                      │
      │─────────────────────▶│                      │
      │                      │                      │
      │ 2. Auth Required     │                      │
      │◀─────────────────────│                      │
      │                      │                      │
      │ 3. DCR Registration  │                      │
      │─────────────────────────────────────────────▶│
      │                      │                      │
      │ 4. Client Creds      │                      │
      │◀──────────────────────────────────────────────│
      │                      │                      │
      │ 5. User Auth Flow    │                      │
      │─────────────────────────────────────────────▶│
      │                      │                      │
      │ 6. Access Token      │                      │
      │◀──────────────────────────────────────────────│
      │                      │                      │
      │ 7. MCP Request       │                      │
      │    + Bearer Token    │                      │
      │─────────────────────▶│                      │
      │                      │ 8. Verify Token     │
      │                      │─────────────────────▶│
      │                      │                      │
      │ 9. MCP Response      │                      │
      │◀─────────────────────│                      │
```

### Key Components

1. **AuthKitProvider** - FastMCP's WorkOS integration
   - Provides OAuth discovery metadata
   - Configures JWT token verification
   - Handles authorization server metadata

2. **Dynamic Client Registration** - Automatic client setup
   - No manual client configuration
   - Clients register on-demand
   - Credentials managed automatically

3. **Token Validation** - JWT verification
   - Uses WorkOS public keys
   - Validates signatures and expiration
   - Extracts user claims

## Troubleshooting

### Common Issues

#### "DCR not enabled" Error
**Problem:** Client can't register automatically
**Solution:** Enable Dynamic Client Registration in WorkOS dashboard under Applications → Configuration

#### "Invalid AuthKit domain" Error
**Problem:** Server can't connect to WorkOS
**Solution:**
- Verify domain format: `https://your-project.authkit.app`
- Remove any trailing slashes
- Check for typos in the domain

#### Token Validation Failures
**Problem:** Server rejects valid tokens
**Symptoms:** 401 Unauthorized after successful login
**Solution:**
- Check server logs for specific JWT errors
- Verify AuthKit domain matches exactly
- Ensure server time is synchronized (for token expiration)

#### Browser Doesn't Open
**Problem:** OAuth flow doesn't start
**Solution:**
- Ensure server is running with HTTP transport (not stdio)
- Check client can reach server URL
- Verify DCR is enabled in WorkOS

### Debug Mode

Enable debug logging to troubleshoot:

```python
# In server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Without Auth

To temporarily disable authentication for testing:

1. Don't set the `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN` variable
2. Server will run without authentication
3. Clients can connect directly

## Production Deployment

### HTTPS Setup

For production, use HTTPS:

1. Update `FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL` to your HTTPS URL
2. Deploy behind a reverse proxy (nginx, Caddy)
3. Or use a platform that provides HTTPS (Render, Railway, etc.)

### Security Considerations

- **Never commit `.env` files** - Use `.env.sample` as template
- **Rotate secrets regularly** - WorkOS supports key rotation
- **Use environment variables** - Don't hardcode credentials
- **Enable audit logs** - Monitor authentication events in WorkOS

### Scaling

- Tokens are stateless (JWT) - No session storage needed
- Server can scale horizontally - All instances share WorkOS config
- Client registration is cached - DCR happens once per client

## Advanced Configuration

### Custom Token Validation

To add custom validation logic:

```python
from fastmcp.server.auth.providers.workos import AuthKitProvider

class CustomAuthProvider(AuthKitProvider):
    async def verify_token(self, token: str) -> bool:
        # Call parent verification
        result = await super().verify_token(token)
        if not result:
            return False

        # Add custom checks
        # e.g., check user roles, organization membership, etc.
        return True
```

### Scope-Based Access Control

Control access to specific tools based on scopes:

```python
@mcp.tool(required_scopes=["admin"])
def admin_tool():
    """Only accessible with admin scope"""
    pass
```

## Resources

- [WorkOS Documentation](https://workos.com/docs)
- [FastMCP Auth Guide](https://docs.gofastmcp.com/servers/auth)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Reddit MCP Issues](https://github.com/king-of-the-grackles/reddit-research-mcp/issues)

## Support

- WorkOS Support: support@workos.com
- Reddit MCP Issues: GitHub Issues
- FastMCP Discord: [Join Discord](https://discord.gg/fastmcp)