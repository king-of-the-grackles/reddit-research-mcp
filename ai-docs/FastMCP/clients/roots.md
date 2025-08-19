# Client Roots

> Provide local context and resource boundaries to MCP servers.

export const VersionBadge = ({version}) => {
  return <code className="version-badge-container">
            <p className="version-badge">
                <span className="version-badge-label">New in version:</span>
                <code className="version-badge-version">{version}</code>
            </p>
        </code>;
};

<VersionBadge version="2.0.0" />

Roots are a way for clients to inform servers about the resources they have access to. Servers can use this information to adjust behavior or provide more relevant responses.

## Setting Static Roots

Provide a list of roots when creating the client:

<CodeGroup>
  ```python Static Roots
  from fastmcp import Client

  client = Client(
      "my_mcp_server.py",
      roots=["/path/to/root1", "/path/to/root2"]
  )
  ```

  ```python Dynamic Roots Callback
  from fastmcp import Client
  from fastmcp.client.roots import RequestContext

  async def roots_callback(context: RequestContext) -> list[str]:
      print(f"Server requested roots (Request ID: {context.request_id})")
      return ["/path/to/root1", "/path/to/root2"]

  client = Client(
      "my_mcp_server.py",
      roots=roots_callback
  )
  ```
</CodeGroup>