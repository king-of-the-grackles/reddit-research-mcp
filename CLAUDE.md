# Reddit Research MCP Server - Development Guide

## Project Overview

This is a Python MCP server built with FastMCP that provides Reddit research capabilities. It's published to:
- **PyPI**: `reddit-research-mcp`
- **MCP Registry**: `io.github.king-of-the-grackles/reddit-research-mcp`

## Key Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python package configuration, version, dependencies |
| `server.json` | MCP Registry configuration |
| `README.md` | Must contain `mcp-name:` line for registry validation |
| `.github/workflows/publish-mcp.yml` | CI/CD for PyPI + MCP Registry publishing |

## Releasing New Versions

### Automated Release Process

1. **Update versions** in both files (must match):
   - `pyproject.toml`: `version = "X.Y.Z"`
   - `server.json`: `"version": "X.Y.Z"` (in both places)

2. **Commit and tag**:
   ```bash
   git add pyproject.toml server.json
   git commit -m "chore: bump version to X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

3. **GitHub Actions** automatically:
   - Builds the Python package
   - Publishes to PyPI
   - Updates server.json version from tag
   - Authenticates to MCP Registry via GitHub OIDC
   - Publishes to MCP Registry

### Required GitHub Secrets

- `PYPI_TOKEN`: PyPI API token scoped to `reddit-research-mcp` package

## MCP Registry Requirements

### server.json Schema

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-10-17/server.schema.json",
  "name": "io.github.king-of-the-grackles/reddit-research-mcp",
  "description": "...",
  "repository": {
    "url": "https://github.com/king-of-the-grackles/reddit-research-mcp",
    "source": "github"
  },
  "version": "1.0.1",
  "packages": [
    {
      "registryType": "pypi",
      "identifier": "reddit-research-mcp",
      "version": "1.0.1",
      "runtimeHint": "uvx",
      "transport": {
        "type": "stdio"
      }
    }
  ]
}
```

### README.md Requirement

The README **must** contain this line (typically at the very top):

```
mcp-name: io.github.king-of-the-grackles/reddit-research-mcp
```

This is used by the MCP Registry to validate PyPI package ownership. The name must exactly match the `name` field in `server.json`.

### Authentication

The server name format determines authentication:
- `io.github.{username}/*` → GitHub authentication (OAuth or OIDC)
- `com.example.*/*` → Domain-based authentication (DNS or HTTP)

This project uses GitHub-based auth via OIDC in CI/CD.

## Manual Publishing (if needed)

```bash
# Install CLI
brew install mcp-publisher

# Authenticate (interactive)
mcp-publisher login github

# Publish
mcp-publisher publish
```

## Common Issues

### "PyPI package ownership validation failed"

The `mcp-name:` line in README.md doesn't match `server.json` name. Ensure they're identical.

### "Cannot publish duplicate version"

PyPI and MCP Registry don't allow re-uploading the same version. Bump the version number.

### Workflow not triggering

If the workflow file was added in the same commit as the tag, delete and recreate the tag:
```bash
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Development

```bash
# Install dependencies
uv sync

# Run locally
uv run python -m src.server

# Build package
uv build

# Run tests
uv run pytest
```

## Links

- [MCP Registry](https://registry.modelcontextprotocol.io/)
- [PyPI Package](https://pypi.org/project/reddit-research-mcp/)
- [GitHub Repository](https://github.com/king-of-the-grackles/reddit-research-mcp)
- [MCP Registry Publishing Guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx)
