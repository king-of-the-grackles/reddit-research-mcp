# Claude Code MCP Server Installation Instructions

## Adding reddit-mcp-poc to Claude Code

Follow these steps to add the reddit-mcp-poc MCP server to your Claude Code configuration:

### Prerequisites
- Ensure you have `uv` installed and the FastMCP server is working locally
- Test that the server starts correctly by running the command directly in terminal

### Installation Steps

1. **Add the MCP server to Claude Code:**
   ```bash
   claude mcp add -s user -t stdio reddit-mcp-poc uv run fastmcp run /Users/chrisivester/Documents/mbp-obsidian-vault/02-Projects/software-projects/MCP/reddit-mcp-poc/reddit-mcp-poc/src/server.py
   ```

2. **Verify the installation:**
   ```bash
   claude mcp list
   ```
   
   You should see `reddit-mcp-poc` listed with a ✓ Connected status.

### Troubleshooting

**If you see a "Failed to connect" status:**
- Check that the path to your server.py file is correct and complete
- Ensure there are no line breaks or truncation in the command path
- Remove and re-add the server if the path was truncated:
  ```bash
  claude mcp remove -s user reddit-mcp-poc
  claude mcp add -s user -t stdio reddit-mcp-poc uv run fastmcp run [FULL_PATH_TO_SERVER.PY]
  ```

**Common Issues:**
- **Path truncation**: Make sure to copy the full path without any line breaks
- **Command not found**: Verify that `uv` is installed and accessible in your PATH
- **Server not starting**: Test the command directly in terminal first before adding to Claude Code

### Configuration Details
- **Scope**: User-level configuration (`-s user`)
- **Transport**: STDIO (`-t stdio`)
- **Server Name**: `reddit-mcp-poc`