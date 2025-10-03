# FastMCP Context Integration - Progress & Logging

**Status:** Draft
**Created:** 2025-10-02
**Owner:** Engineering Team

## Executive Summary

This specification outlines the integration of FastMCP's Context API to add progress monitoring, structured logging, and enhanced error context to the Reddit MCP server. These improvements will provide real-time visibility into server operations for debugging and user feedback.

## Background

The Reddit MCP server currently lacks visibility into long-running operations. Users cannot see progress during multi-step tasks like discovering subreddits or fetching posts from multiple communities. Server-side logging and error context are not surfaced to clients, making debugging difficult.

FastMCP's Context API provides built-in support for:
- **Progress reporting**: `ctx.report_progress(current, total, message)`
- **Structured logging**: `ctx.info()`, `ctx.warning()`, `ctx.error()`
- **Error context**: Rich error information with operation details

## Goals

1. **Progress Monitoring**: Report real-time progress during multi-step operations
2. **Structured Logging**: Surface server logs to clients at appropriate severity levels
3. **Enhanced Errors**: Provide detailed error context including operation name, type, and recovery suggestions
4. **Developer Experience**: Maintain clean, testable code with minimal complexity

## Non-Goals

- Frontend client implementation (separate project)
- UI component development (separate project)
- Metrics collection and export features
- Resource access tracking
- Sampling request monitoring

## Technical Design

### Phase 1: Context Integration (Days 1-2)

**Objective**: Enable all tool functions to receive FastMCP Context

#### Implementation Steps

1. **Update Tool Signatures**
   - Add required `Context` parameter to all functions in `src/tools/`
   - Pattern: `def tool_name(param: str, ctx: Context) -> dict:`
   - FastMCP automatically injects context when tools are called with `@mcp.tool` decorator

2. **Update execute_operation()**
   - Ensure context flows through to tool functions
   - No changes needed - FastMCP handles injection automatically

#### Files to Modify
- `src/tools/discover.py`
- `src/tools/posts.py`
- `src/tools/comments.py`
- `src/tools/search.py`
- `src/server.py`

#### Code Example

**Before:**
```python
def discover_subreddits(query: str, limit: int = 10) -> dict:
    results = search_vector_db(query, limit)
    return {"subreddits": results}
```

**After:**
```python
def discover_subreddits(
    query: str,
    limit: int = 10,
    ctx: Context
) -> dict:
    results = search_vector_db(query, limit)
    return {"subreddits": results}
```

### Phase 2: Progress Monitoring (Days 3-4)

**Objective**: Report progress during long-running operations

#### Progress Events

**discover_subreddits** - Vector search progress:
```python
for i, result in enumerate(search_results):
    ctx.report_progress(
        progress=i + 1,
        total=limit,
        message=f"Analyzing r/{result.name}"
    )
```

**fetch_multiple_subreddits** - Batch fetch progress:
```python
for i, subreddit in enumerate(subreddit_names):
    ctx.report_progress(
        progress=i + 1,
        total=len(subreddit_names),
        message=f"Fetching r/{subreddit}"
    )
    # Fetch posts...
```

**fetch_submission_with_comments** - Comment loading progress:
```python
ctx.report_progress(
    progress=len(comments),
    total=comment_limit,
    message=f"Loading comments ({len(comments)}/{comment_limit})"
)
```

#### Files to Modify
- `src/tools/discover.py` - Add progress during vector search iteration
- `src/tools/posts.py` - Add progress per subreddit in batch operations
- `src/tools/comments.py` - Add progress during comment tree traversal

### Phase 3: Structured Logging (Days 5-6)

**Objective**: Surface server-side information to clients via logs

#### Logging Events by Operation

**Discovery Operations** (`src/tools/discover.py`):
```python
ctx.info(f"Starting discovery for topic: {query}")
ctx.info(f"Found {len(results)} communities (avg confidence: {avg_conf:.2f})")

if avg_conf < 0.5:
    ctx.warning(f"Low confidence results (<0.5) for query: {query}")
```

**Fetch Operations** (`src/tools/posts.py`):
```python
ctx.info(f"Fetching {limit} posts from r/{subreddit_name}")
ctx.info(f"Successfully fetched {len(posts)} posts from r/{subreddit_name}")

# Rate limit warnings
if remaining_requests < 10:
    ctx.warning(f"Rate limit approaching: {remaining_requests}/60 requests remaining")

# Error logging
ctx.error(f"Failed to fetch r/{subreddit_name}: {str(e)}", extra={
    "subreddit": subreddit_name,
    "error_type": type(e).__name__
})
```

**Search Operations** (`src/tools/search.py`):
```python
ctx.info(f"Searching r/{subreddit_name} for: {query}")
ctx.debug(f"Search parameters: sort={sort}, time_filter={time_filter}")
```

**Comment Operations** (`src/tools/comments.py`):
```python
ctx.info(f"Fetching comments for submission: {submission_id}")
ctx.info(f"Loaded {len(comments)} comments (sort: {comment_sort})")
```

#### Log Levels

- **DEBUG**: Internal operation details, parameter values
- **INFO**: Operation start/completion, success metrics
- **WARNING**: Rate limits, low confidence scores, degraded functionality
- **ERROR**: Operation failures, API errors, exceptions

#### Files to Modify
- `src/tools/discover.py` - Confidence scores, discovery metrics
- `src/tools/posts.py` - Fetch success/failure, rate limit warnings
- `src/tools/comments.py` - Comment analysis metrics
- `src/tools/search.py` - Search operation logging

### Phase 4: Enhanced Error Handling (Days 7-8)

**Objective**: Provide detailed error context for debugging and recovery

#### Error Context Pattern

**Current Implementation:**
```python
except Exception as e:
    return {
        "success": False,
        "error": str(e),
        "recovery": suggest_recovery(operation_id, e)
    }
```

**Enhanced Implementation:**
```python
except Exception as e:
    error_type = type(e).__name__

    # Log error with context
    ctx.error(
        f"Operation failed: {operation_id}",
        extra={
            "operation": operation_id,
            "error_type": error_type,
            "parameters": parameters,
            "timestamp": datetime.now().isoformat()
        }
    )

    return {
        "success": False,
        "error": str(e),
        "error_type": error_type,
        "operation": operation_id,
        "parameters": parameters,
        "recovery": suggest_recovery(operation_id, e),
        "timestamp": datetime.now().isoformat()
    }
```

#### Error Categories & Recovery Suggestions

| Error Type | Recovery Suggestion |
|------------|-------------------|
| 404 / Not Found | "Verify subreddit name or use discover_subreddits" |
| 429 / Rate Limited | "Reduce limit parameter or wait 30s before retrying" |
| 403 / Private | "Subreddit is private - try other communities" |
| Validation Error | "Check parameters match schema from get_operation_schema" |
| Network Error | "Check internet connection and retry" |

#### Files to Modify
- `src/server.py` - Enhanced `execute_operation()` error handling
- `src/tools/*.py` - Operation-specific error logging

### Phase 5: Testing & Validation (Days 9-10)

**Objective**: Ensure all instrumentation works correctly

#### Test Coverage

**Context Integration Tests** (`tests/test_context_integration.py`):
```python
async def test_context_injected():
    """Verify context is properly injected into tools"""

async def test_progress_events_emitted():
    """Verify progress events during multi-step operations"""

async def test_log_messages_captured():
    """Verify logs at appropriate severity levels"""

async def test_error_context_included():
    """Verify error responses include operation details"""
```

**Updated Tool Tests** (`tests/test_tools.py`):
- Verify tools receive and use context properly
- Check progress reporting frequency (≥5 events per operation)
- Validate log message content and levels
- Ensure error context is complete

#### Files to Create/Modify
- Create: `tests/test_context_integration.py`
- Modify: `tests/test_tools.py`

## Implementation Details

### Context Parameter Pattern

FastMCP automatically injects Context when tools are decorated with `@mcp.tool`:

```python
@mcp.tool
def my_tool(param: str, ctx: Context) -> dict:
    # Context is automatically injected
    ctx.info("Tool started")
    ctx.report_progress(1, 10, "Processing")
    return {"result": "data"}
```

For functions called internally (not decorated), Context must be passed explicitly:

```python
def internal_function(param: str, ctx: Context) -> dict:
    ctx.info("Internal operation")
    return {"result": "data"}
```

### Progress Reporting Best Practices

1. **Report at regular intervals**: Every iteration in loops
2. **Provide descriptive messages**: "Fetching r/Python" not "Step 1"
3. **Include total when known**: `ctx.report_progress(5, 10, msg)`
4. **Use meaningful units**: Report actual progress (items processed) not arbitrary percentages

### Logging Best Practices

1. **Use appropriate levels**: INFO for normal ops, WARNING for issues, ERROR for failures
2. **Include context in extra**: `ctx.error(msg, extra={"operation": "name"})`
3. **Structured messages**: Consistent format for parsing
4. **Avoid spam**: Log meaningful events, not every line

### Error Handling Best Practices

1. **Specific exception types**: Catch specific errors when possible
2. **Include operation context**: Always log which operation failed
3. **Actionable recovery**: Provide specific steps to resolve
4. **Preserve stack traces**: Log full error details in extra

## Success Criteria

### Functional Requirements
- ✅ All tool functions accept required Context parameter
- ✅ Progress events emitted during multi-step operations (≥5 per operation)
- ✅ Server logs at appropriate severity levels (DEBUG/INFO/WARNING/ERROR)
- ✅ Error responses include operation name, type, and recovery suggestions
- ✅ MCP client compatibility maintained (Claude, ChatGPT, etc.)

### Technical Requirements
- ✅ All existing tests pass with new instrumentation
- ✅ New integration tests verify context functionality
- ✅ No performance degradation (progress/logging overhead <5%)
- ✅ Type hints maintained throughout

### Quality Requirements
- ✅ Code follows FastMCP patterns from documentation
- ✅ Logging messages are clear and actionable
- ✅ Error recovery suggestions are specific and helpful
- ✅ Progress messages provide meaningful status updates

## File Summary

### Files to Create
- `tests/test_context_integration.py` - New integration tests

### Files to Modify
- `src/tools/discover.py` - Context, progress, logging
- `src/tools/posts.py` - Context, progress, logging
- `src/tools/comments.py` - Context, progress, logging
- `src/tools/search.py` - Context, logging
- `src/server.py` - Enhanced error handling in execute_operation
- `tests/test_tools.py` - Updated tests for context integration

### Files Not Modified
- `src/config.py` - No changes needed
- `src/models.py` - No changes needed
- `src/resources.py` - No changes needed (future enhancement)
- `src/chroma_client.py` - No changes needed

## Dependencies

### Required
- FastMCP ≥2.0.0 (already installed)
- Python ≥3.10 (already using)
- Context API support (available in FastMCP)

### Optional
- No additional dependencies required

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Performance overhead from logging | Low | Log only meaningful events, avoid verbose debug logs in production |
| Too many progress events | Low | Limit to 5-10 events per operation |
| Breaking MCP client compatibility | Low | Context changes are server-side only; MCP protocol unchanged |
| Testing complexity | Low | Use FastMCP's in-memory transport for tests |

## Backward Compatibility

**MCP Client Compatibility**: Changes are server-side implementation only. The MCP protocol interface remains unchanged, ensuring compatibility with all MCP clients including Claude, ChatGPT, and others. Context injection is handled by FastMCP's decorator system and is transparent to clients.

## Future Enhancements

Following this implementation, future phases could include:

1. **Resource Access Tracking** - Monitor `ctx.read_resource()` calls
2. **Sampling Monitoring** - Track `ctx.sample()` operations
3. **Metrics Collection** - Aggregate operation timing and success rates
4. **Client Integration** - Frontend components to display progress/logs

These are out of scope for this specification.

## References

- [FastMCP Context API Documentation](../ai-docs/fastmcp/docs/python-sdk/fastmcp-server-context.mdx)
- [FastMCP Progress Monitoring](../ai-docs/fastmcp/docs/clients/progress.mdx)
- [FastMCP Logging](../ai-docs/fastmcp/docs/clients/logging.mdx)
- Current Implementation: `src/server.py`
- Original UX Improvements Spec: `../frontend-reddit-research-mcp/specs/002-ux-improvements-fastmcp-patterns/spec.md`
