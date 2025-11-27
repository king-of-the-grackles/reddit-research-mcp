# Dual-Issuer Authentication for Reddit MCP Server

## Overview

The MCP server now supports **both OAuth/DCR tokens AND session tokens** from Descope. This allows:

1. **Claude Desktop** (and other MCP clients) to authenticate via OAuth2 DCR flow
2. **Agent backend** to forward user session tokens from the Descope SDK

## The Problem We Solved

Previously, the server only accepted tokens with issuer format:
```
https://api.descope.com/v1/apps/{project_id}
```

But Descope session tokens (from `getSessionToken()` in the SDK) use a different issuer format:
```
{project_id}
```
(Just the project ID, no URL - per [Descope Session Management docs](https://docs.descope.com/authorization/session-management))

This caused 401 `invalid_token` errors when forwarding session tokens from the agent backend.

## Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Server                                   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              MultiIssuerJWTVerifier                      │    │
│  │                                                          │    │
│  │  Accepts tokens with EITHER issuer:                      │    │
│  │  ✓ https://api.descope.com/v1/apps/{project_id}         │    │
│  │  ✓ {project_id}                                          │    │
│  │                                                          │    │
│  │  Uses same JWKS for signature validation:                │    │
│  │  https://api.descope.com/{project_id}/.well-known/jwks  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              DescopeProvider                             │    │
│  │                                                          │    │
│  │  Still provides:                                         │    │
│  │  ✓ /.well-known/oauth-authorization-server              │    │
│  │  ✓ /.well-known/oauth-protected-resource                │    │
│  │  ✓ OAuth2 DCR flow support                              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## For the Agent Backend

### How to Forward Session Tokens

When your agent backend receives a request with a Descope session token, forward it to the MCP server as a Bearer token:

```typescript
// In your agent backend
async function callMcpServer(sessionToken: string) {
  const response = await fetch('https://reddit-research-mcp.fastmcp.app/mcp', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${sessionToken}`,  // Session token from Descope SDK
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      // MCP request body
    }),
  });
}
```

### Token Requirements

The session token MUST have:

| Claim | Expected Value | Notes |
|-------|----------------|-------|
| `iss` | `{project_id}` | Just the project ID (e.g., `P33G9OI0uZKubCM9c3RE9KGxPJbn`) |
| `aud` | `{project_id}` | Same as issuer |
| `exp` | Future timestamp | Token must not be expired |
| `sub` | User ID | Used as `client_id` in the MCP context |

### Verifying Your Token Format

You can decode a session token to verify its format:

```bash
# Decode the payload (middle part) of a JWT
echo "YOUR_SESSION_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq '.'
```

Expected output for a **session token**:
```json
{
  "iss": "P33G9OI0uZKubCM9c3RE9KGxPJbn",
  "sub": "U2RG6grrbT3REKYqk5yC4SjkMqzA",
  "aud": "P33G9OI0uZKubCM9c3RE9KGxPJbn",
  "exp": 1692304651,
  "iat": 1692304051,
  ...
}
```

Expected output for an **OAuth token** (from DCR flow):
```json
{
  "iss": "https://api.descope.com/v1/apps/P33G9OI0uZKubCM9c3RE9KGxPJbn",
  "sub": "client_abc123",
  "aud": "P33G9OI0uZKubCM9c3RE9KGxPJbn",
  "exp": 1692304651,
  ...
}
```

**Both formats are now accepted by the MCP server.**

## Testing the Integration

### 1. Test Health Endpoint (No Auth)

```bash
curl https://reddit-research-mcp.fastmcp.app/health
```

Expected response:
```json
{
  "status": "ok",
  "server": "Reddit MCP",
  "version": "1.0.0",
  "auth_required": true
}
```

### 2. Test with Session Token

```bash
# Replace with actual session token from Descope SDK
SESSION_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST https://reddit-research-mcp.fastmcp.app/mcp \
  -H "Authorization: Bearer $SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

### 3. Test OAuth Discovery (For Claude Desktop)

```bash
curl https://reddit-research-mcp.fastmcp.app/.well-known/oauth-authorization-server
```

Should return Descope's OAuth metadata (forwarded from Descope).

## Troubleshooting

### Error: 401 `invalid_token`

**Possible causes:**

1. **Token expired** - Check `exp` claim is in the future
2. **Wrong issuer** - Verify `iss` is either:
   - `{project_id}` (session token)
   - `https://api.descope.com/v1/apps/{project_id}` (OAuth token)
3. **Wrong audience** - Verify `aud` matches the project ID
4. **Invalid signature** - Token must be signed by Descope's keys

**Debug steps:**
```bash
# Decode and inspect your token
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq '{iss, aud, exp, sub}'

# Check if token is expired
python3 -c "import time; exp=YOUR_EXP_VALUE; print('Expired' if exp < time.time() else 'Valid')"
```

### Error: Connection refused

The MCP server might not be running. Check:
- Server health: `curl https://reddit-research-mcp.fastmcp.app/health`
- Server info: `curl https://reddit-research-mcp.fastmcp.app/server-info`

### Error: OAuth flow not working (Claude Desktop)

The OAuth metadata endpoint should still work:
```bash
curl https://reddit-research-mcp.fastmcp.app/.well-known/oauth-authorization-server
```

If this fails, the server might not be configured correctly.

## Implementation Details

### Files Changed

| File | Description |
|------|-------------|
| `src/auth/__init__.py` | New auth module |
| `src/auth/multi_issuer_verifier.py` | `MultiIssuerJWTVerifier` class |
| `src/server.py` | Updated to use multi-issuer verifier |

### Configuration

The server reads these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DESCOPE_PROJECT_ID` | Your Descope project ID | `P33G9OI0uZKubCM9c3RE9KGxPJbn` |
| `DESCOPE_BASE_URL` | Descope API base URL | `https://api.descope.com` |
| `SERVER_URL` | Public URL of MCP server | `https://reddit-research-mcp.fastmcp.app` |

### Valid Issuers (Auto-configured)

The server automatically accepts tokens from:
1. `{DESCOPE_BASE_URL}/v1/apps/{DESCOPE_PROJECT_ID}` - OAuth tokens
2. `{DESCOPE_PROJECT_ID}` - Session tokens

## Questions?

If you encounter issues not covered here, check:
1. The token format matches expected claims
2. The Descope project ID matches between frontend and MCP server
3. The token is not expired

For server-side issues, check the MCP server logs for detailed error messages.
