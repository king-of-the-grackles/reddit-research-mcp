# Langfuse Observability Integration

This Reddit MCP server includes optional Langfuse observability integration for comprehensive tracing and monitoring of all operations.

## Features

- **Complete Operation Tracking**: Every MCP operation is traced through the three-layer architecture
- **Performance Monitoring**: Track latencies and identify bottlenecks
- **Error Tracking**: Capture failures with full context
- **Reddit-Specific Metadata**: Track subreddits, confidence scores, post counts, and more
- **W3C-Compliant Traces**: All trace IDs follow the W3C Trace Context standard
- **Graceful Degradation**: Server continues to function even if Langfuse is unavailable

## Setup

### 1. Install Dependencies

The Langfuse dependency is already included in the project:

```bash
uv sync
```

### 2. Configure Environment Variables

Add your Langfuse credentials to your `.env` file or environment:

```bash
# Required for observability
export LANGFUSE_PUBLIC_KEY=pk-lf-...
export LANGFUSE_SECRET_KEY=sk-lf-...

# Optional configuration
export LANGFUSE_HOST=https://cloud.langfuse.com  # EU region (default)
# export LANGFUSE_HOST=https://us.cloud.langfuse.com  # US region
export LANGFUSE_ENVIRONMENT=production  # or development, staging
export LANGFUSE_RELEASE=v1.0.0  # Your release version

# Control observability
export LANGFUSE_ENABLED=true  # Set to false to disable
export LANGFUSE_DEBUG=false  # Set to true for verbose logging
export LANGFUSE_VERIFY_CONNECTION=false  # Set to true to verify connection on startup
```

### 3. Run the Server

Observability will be automatically enabled if credentials are configured:

```bash
uv run src/server.py
```

You'll see one of these messages on startup:
- `Langfuse observability enabled` - Tracing is active
- `Langfuse credentials not found. Observability disabled.` - No credentials configured
- `Running without observability` - Explicitly disabled or error occurred

## What Gets Tracked

### Operations
- **discover_operations**: Discovery of available operations
- **get_operation_schema**: Schema retrieval with operation_id
- **execute_operation**: Full execution with parameters and results

### Metadata Captured
- Operation type and ID
- Subreddit names and confidence scores
- Post/comment counts
- Search queries and filters
- Time ranges and sort options
- Error recovery suggestions
- Tool metadata (tags, enabled status, description)
- Server information

### Performance Metrics
- Operation duration in milliseconds
- Success/failure status
- Error types and messages

## Trace Structure

```
Trace: Reddit MCP Request
├── Span: discover_operations
├── Span: get_operation_schema
│   └── metadata: {operation_id: "fetch_multiple"}
└── Span: execute_operation
    ├── metadata: {operation_id: "fetch_multiple", subreddits: [...]}
    └── output: {success: true, post_count: 50}
```

## Testing

Run the test suite to verify the integration:

```bash
# Unit tests
uv run pytest tests/test_langfuse_middleware.py -v

# Integration tests (requires Langfuse credentials)
uv run pytest tests/test_integration_langfuse.py -v

# Performance tests
uv run tests/test_performance.py

# Resilience tests
uv run pytest tests/test_resilience.py -v
```

## Architecture

The integration uses FastMCP's middleware system:

1. **LangfuseMiddleware** intercepts all MCP operations
2. **Context Enhancement** uses `fastmcp_context` to access tool metadata
3. **W3C Trace IDs** ensure compatibility with OpenTelemetry standards
4. **Graceful Degradation** continues operation even if Langfuse fails

## Troubleshooting

### No traces appearing in Langfuse
1. Check credentials are correct
2. Verify `LANGFUSE_HOST` matches your region
3. Set `LANGFUSE_VERIFY_CONNECTION=true` to test connection
4. Check `LANGFUSE_ENABLED` is not set to `false`

### Performance impact
- Middleware overhead is typically <10ms per operation
- Traces are batched and sent asynchronously
- Set `LANGFUSE_ENABLED=false` to disable if needed

### Server won't start
- The server will start even without Langfuse
- Check logs for specific error messages
- Ensure `langfuse>=2.50.0` is installed

## Benefits

1. **Performance Optimization**: Identify slow operations and optimize them
2. **Error Investigation**: Full context for debugging failures
3. **Usage Analytics**: Understand which operations are most used
4. **Cost Tracking**: Monitor Reddit API usage patterns
5. **Quality Assurance**: Ensure consistent operation performance