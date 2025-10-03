# Phase 1: Context Integration - Detailed Specification

**Status:** Ready for Implementation
**Created:** 2025-10-02
**Phase Duration:** Days 1-2
**Owner:** Engineering Team
**Parent Spec:** [003-fastmcp-context-integration.md](./003-fastmcp-context-integration.md)

## Objective

Enable all tool functions in the Reddit MCP server to receive and utilize FastMCP's Context API. This phase establishes the foundation for progress monitoring, structured logging, and enhanced error handling in subsequent phases.

## Background

FastMCP's Context API is automatically injected into tool functions decorated with `@mcp.tool`. The context object provides methods for:
- Progress reporting: `ctx.report_progress(current, total, message)`
- Structured logging: `ctx.info()`, `ctx.warning()`, `ctx.error()`, `ctx.debug()`
- Error context: Rich error information via structured logging

To use these features, all tool functions must accept a `Context` parameter. This phase focuses solely on adding the context parameter to function signatures—no actual usage of context methods yet.

## Goals

1. **Add Context Parameter**: Update all tool function signatures to accept `ctx: Context`
2. **Maintain Type Safety**: Preserve all type hints and ensure type checking passes
3. **Verify Auto-Injection**: Confirm FastMCP's decorator system injects context correctly
4. **Test Compatibility**: Ensure all existing tests pass with updated signatures

## Non-Goals

- Using context methods (progress, logging, error handling) - Phase 2+
- Adding new tool functions or operations
- Modifying MCP protocol or client interfaces
- Performance optimization or refactoring

## Implementation Details

### Context Parameter Pattern

FastMCP automatically injects `Context` when tools are decorated with `@mcp.tool`:

```python
from fastmcp import Context

@mcp.tool
def my_tool(param: str, ctx: Context) -> dict:
    # Context is automatically injected by FastMCP
    # No usage required in Phase 1 - just accept the parameter
    return {"result": "data"}
```

**Important Notes:**
- Context is a **required** parameter (not optional)
- Position in signature: Place after all other parameters
- Type hint must be `Context` (imported from `fastmcp`)
- No default value needed - FastMCP injects automatically

### Files to Modify

#### 1. `src/tools/discover.py`

**Functions to update:**
- `discover_subreddits(query: str, limit: int = 10) -> dict`
- `get_subreddit_info(subreddit_name: str) -> dict`

**Before:**
```python
def discover_subreddits(query: str, limit: int = 10) -> dict:
    """Search vector database for relevant subreddits."""
    results = search_vector_db(query, limit)
    return {
        "subreddits": [format_subreddit(r) for r in results],
        "count": len(results)
    }
```

**After:**
```python
from fastmcp import Context

def discover_subreddits(
    query: str,
    limit: int = 10,
    ctx: Context
) -> dict:
    """Search vector database for relevant subreddits."""
    # Phase 1: Accept context but don't use it yet
    results = search_vector_db(query, limit)
    return {
        "subreddits": [format_subreddit(r) for r in results],
        "count": len(results)
    }
```

**Estimated Time:** 30 minutes

---

#### 2. `src/tools/posts.py`

**Functions to update:**
- `fetch_subreddit_posts(subreddit_name: str, limit: int = 10, time_filter: str = "all", sort: str = "hot") -> dict`
- `fetch_multiple_subreddits(subreddit_names: list[str], limit_per_subreddit: int = 10) -> dict`
- `get_post_details(post_id: str) -> dict`

**Before:**
```python
def fetch_subreddit_posts(
    subreddit_name: str,
    limit: int = 10,
    time_filter: str = "all",
    sort: str = "hot"
) -> dict:
    """Fetch posts from a subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    posts = list(subreddit.hot(limit=limit))
    return {"posts": [format_post(p) for p in posts]}
```

**After:**
```python
from fastmcp import Context

def fetch_subreddit_posts(
    subreddit_name: str,
    limit: int = 10,
    time_filter: str = "all",
    sort: str = "hot",
    ctx: Context
) -> dict:
    """Fetch posts from a subreddit."""
    # Phase 1: Accept context but don't use it yet
    subreddit = reddit.subreddit(subreddit_name)
    posts = list(subreddit.hot(limit=limit))
    return {"posts": [format_post(p) for p in posts]}
```

**Estimated Time:** 45 minutes

---

#### 3. `src/tools/comments.py`

**Functions to update:**
- `fetch_submission_with_comments(submission_id: str, comment_limit: int = 50, comment_sort: str = "best") -> dict`
- `get_comment_thread(comment_id: str, depth: int = 5) -> dict`

**Before:**
```python
def fetch_submission_with_comments(
    submission_id: str,
    comment_limit: int = 50,
    comment_sort: str = "best"
) -> dict:
    """Fetch submission and its comments."""
    submission = reddit.submission(id=submission_id)
    comments = fetch_comments(submission, comment_limit, comment_sort)
    return {
        "submission": format_submission(submission),
        "comments": comments
    }
```

**After:**
```python
from fastmcp import Context

def fetch_submission_with_comments(
    submission_id: str,
    comment_limit: int = 50,
    comment_sort: str = "best",
    ctx: Context
) -> dict:
    """Fetch submission and its comments."""
    # Phase 1: Accept context but don't use it yet
    submission = reddit.submission(id=submission_id)
    comments = fetch_comments(submission, comment_limit, comment_sort)
    return {
        "submission": format_submission(submission),
        "comments": comments
    }
```

**Estimated Time:** 30 minutes

---

#### 4. `src/tools/search.py`

**Functions to update:**
- `search_subreddit(subreddit_name: str, query: str, limit: int = 10, time_filter: str = "all", sort: str = "relevance") -> dict`

**Before:**
```python
def search_subreddit(
    subreddit_name: str,
    query: str,
    limit: int = 10,
    time_filter: str = "all",
    sort: str = "relevance"
) -> dict:
    """Search within a specific subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    results = subreddit.search(query, limit=limit, time_filter=time_filter, sort=sort)
    return {"results": [format_post(r) for r in results]}
```

**After:**
```python
from fastmcp import Context

def search_subreddit(
    subreddit_name: str,
    query: str,
    limit: int = 10,
    time_filter: str = "all",
    sort: str = "relevance",
    ctx: Context
) -> dict:
    """Search within a specific subreddit."""
    # Phase 1: Accept context but don't use it yet
    subreddit = reddit.subreddit(subreddit_name)
    results = subreddit.search(query, limit=limit, time_filter=time_filter, sort=sort)
    return {"results": [format_post(r) for r in results]}
```

**Estimated Time:** 20 minutes

---

#### 5. `src/server.py`

**Changes needed:**
- Import Context from fastmcp
- Verify execute_operation passes context to tools (FastMCP handles this automatically)
- No signature changes needed for execute_operation itself

**Before:**
```python
# At top of file
from fastmcp import FastMCP

mcp = FastMCP("Reddit Research MCP")
```

**After:**
```python
# At top of file
from fastmcp import FastMCP, Context

mcp = FastMCP("Reddit Research MCP")

# No other changes needed - FastMCP auto-injects context
```

**Estimated Time:** 10 minutes

---

### Helper Functions

**Internal helper functions** (not decorated with `@mcp.tool`) that need context should also accept it:

```python
# Helper function called by tool
def fetch_comments(submission, limit: int, sort: str, ctx: Context) -> list:
    """Internal helper for fetching comments."""
    # Phase 1: Accept context but don't use it yet
    submission.comment_sort = sort
    submission.comments.replace_more(limit=0)
    return list(submission.comments.list()[:limit])
```

**Functions to check:**
- `src/tools/discover.py`: `search_vector_db()`, `format_subreddit()`
- `src/tools/posts.py`: `format_post()`
- `src/tools/comments.py`: `fetch_comments()`, `format_comment()`

**Decision rule:** Only add context to helpers that will need it in Phase 2+ (for logging/progress). Review each helper and add context parameter if:
1. It performs I/O operations (API calls, database queries)
2. It contains loops that could benefit from progress reporting
3. It has error handling that would benefit from context logging

**Estimated Time:** 30 minutes

---

## Testing Strategy

### Unit Tests

Update existing tests in `tests/test_tools.py` to pass context:

**Before:**
```python
def test_discover_subreddits():
    result = discover_subreddits("machine learning", limit=5)
    assert result["count"] == 5
```

**After:**
```python
from unittest.mock import Mock
from fastmcp import Context

def test_discover_subreddits():
    # Create mock context for testing
    mock_ctx = Mock(spec=Context)

    result = discover_subreddits("machine learning", limit=5, ctx=mock_ctx)
    assert result["count"] == 5
```

**Note:** FastMCP provides test utilities for creating context objects. Consult FastMCP testing documentation for best practices.

### Integration Tests

**New test file:** `tests/test_context_integration.py`

```python
import pytest
from unittest.mock import Mock
from fastmcp import Context

from src.tools.discover import discover_subreddits
from src.tools.posts import fetch_subreddit_posts
from src.tools.comments import fetch_submission_with_comments
from src.tools.search import search_subreddit

@pytest.fixture
def mock_context():
    """Create a mock Context object for testing."""
    return Mock(spec=Context)

def test_discover_accepts_context(mock_context):
    """Verify discover_subreddits accepts context parameter."""
    result = discover_subreddits("test query", limit=5, ctx=mock_context)
    assert "subreddits" in result

def test_fetch_posts_accepts_context(mock_context):
    """Verify fetch_subreddit_posts accepts context parameter."""
    result = fetch_subreddit_posts("python", limit=5, ctx=mock_context)
    assert "posts" in result

def test_fetch_comments_accepts_context(mock_context):
    """Verify fetch_submission_with_comments accepts context parameter."""
    result = fetch_submission_with_comments("test_id", comment_limit=10, ctx=mock_context)
    assert "submission" in result
    assert "comments" in result

def test_search_accepts_context(mock_context):
    """Verify search_subreddit accepts context parameter."""
    result = search_subreddit("python", "testing", limit=5, ctx=mock_context)
    assert "results" in result
```

**Estimated Time:** 1 hour

---

## Success Criteria

### Phase 1 Completion Checklist

- [ ] All functions in `src/tools/discover.py` accept `ctx: Context`
- [ ] All functions in `src/tools/posts.py` accept `ctx: Context`
- [ ] All functions in `src/tools/comments.py` accept `ctx: Context`
- [ ] All functions in `src/tools/search.py` accept `ctx: Context`
- [ ] `src/server.py` imports Context from fastmcp
- [ ] All relevant helper functions accept context parameter
- [ ] All existing unit tests updated to pass context
- [ ] New integration tests created in `tests/test_context_integration.py`
- [ ] All tests pass: `pytest tests/`
- [ ] Type checking passes: `mypy src/`
- [ ] No regressions in existing functionality

### Validation Commands

```bash
# Run all tests
pytest tests/ -v

# Type checking
mypy src/

# Verify no breaking changes
pytest tests/test_tools.py -v
```

---

## Implementation Order

1. **Day 1 Morning (2 hours)**
   - Update `src/tools/discover.py` (30 min)
   - Update `src/tools/posts.py` (45 min)
   - Update `src/tools/comments.py` (30 min)
   - Update `src/tools/search.py` (20 min)

2. **Day 1 Afternoon (2 hours)**
   - Update `src/server.py` (10 min)
   - Review and update helper functions (30 min)
   - Update existing unit tests (1 hour)
   - Run full test suite and fix issues (20 min)

3. **Day 2 Morning (2 hours)**
   - Create `tests/test_context_integration.py` (1 hour)
   - Run all validation commands (30 min)
   - Code review and cleanup (30 min)

4. **Day 2 Afternoon (1 hour)**
   - Final testing and validation
   - Documentation updates (if needed)
   - Prepare for Phase 2

**Total Estimated Time:** 7 hours over 2 days

---

## Dependencies

### Required Packages
- `fastmcp>=2.0.0` (already installed)
- `pytest>=7.0.0` (already installed for testing)
- `mypy>=1.0.0` (recommended for type checking)

### External Dependencies
- None - this phase only modifies function signatures

### Knowledge Prerequisites
- FastMCP decorator system and auto-injection
- Python type hints and type checking
- Pytest fixture system for mocking

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing tests | Medium | High | Update tests incrementally, verify after each file |
| Type checking errors | Low | Medium | Use `Mock(spec=Context)` for type-safe mocking |
| FastMCP auto-injection not working | Low | High | Verify with simple test case first; consult docs |
| Forgetting helper functions | Medium | Medium | Grep codebase for all function definitions, review systematically |

---

## Code Review Checklist

Before marking Phase 1 complete, verify:

- [ ] All tool functions have `ctx: Context` as last parameter
- [ ] Type hints are correct: `ctx: Context` (not `ctx: Optional[Context]`)
- [ ] Import statements include `from fastmcp import Context`
- [ ] Helper functions that need context receive it
- [ ] Test mocks use `Mock(spec=Context)` for type safety
- [ ] No actual usage of context methods (that's Phase 2+)
- [ ] All tests pass without errors or warnings
- [ ] Type checking passes with mypy

---

## Next Steps

Upon successful completion of Phase 1:

1. **Phase 2: Progress Monitoring** - Add `ctx.report_progress()` calls
2. **Phase 3: Structured Logging** - Add `ctx.info()`, `ctx.warning()`, `ctx.error()`
3. **Phase 4: Enhanced Error Handling** - Use context in error scenarios
4. **Phase 5: Testing & Validation** - Comprehensive integration testing

---

## References

- [FastMCP Context API Documentation](../ai-docs/fastmcp/docs/python-sdk/fastmcp-server-context.mdx)
- [FastMCP Tool Decorator Pattern](../ai-docs/fastmcp/docs/python-sdk/fastmcp-server-tool.mdx)
- [Parent Specification](./003-fastmcp-context-integration.md)
- Current Implementation: `src/server.py`

---

## Appendix: Complete Example

**Full example showing before/after for a complete tool function:**

**Before (existing code):**
```python
# src/tools/posts.py
from src.reddit_client import reddit

def fetch_subreddit_posts(
    subreddit_name: str,
    limit: int = 10,
    time_filter: str = "all",
    sort: str = "hot"
) -> dict:
    """
    Fetch posts from a subreddit.

    Args:
        subreddit_name: Name of the subreddit
        limit: Number of posts to fetch
        time_filter: Time filter (all, day, week, month, year)
        sort: Sort method (hot, new, top, rising)

    Returns:
        Dictionary with posts and metadata
    """
    try:
        subreddit = reddit.subreddit(subreddit_name)

        # Get posts based on sort method
        if sort == "hot":
            posts = list(subreddit.hot(limit=limit))
        elif sort == "new":
            posts = list(subreddit.new(limit=limit))
        elif sort == "top":
            posts = list(subreddit.top(time_filter=time_filter, limit=limit))
        elif sort == "rising":
            posts = list(subreddit.rising(limit=limit))
        else:
            raise ValueError(f"Invalid sort method: {sort}")

        return {
            "success": True,
            "subreddit": subreddit_name,
            "posts": [format_post(p) for p in posts],
            "count": len(posts)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "subreddit": subreddit_name
        }
```

**After (Phase 1 changes):**
```python
# src/tools/posts.py
from fastmcp import Context
from src.reddit_client import reddit

def fetch_subreddit_posts(
    subreddit_name: str,
    limit: int = 10,
    time_filter: str = "all",
    sort: str = "hot",
    ctx: Context  # ← ONLY CHANGE IN PHASE 1
) -> dict:
    """
    Fetch posts from a subreddit.

    Args:
        subreddit_name: Name of the subreddit
        limit: Number of posts to fetch
        time_filter: Time filter (all, day, week, month, year)
        sort: Sort method (hot, new, top, rising)
        ctx: FastMCP context (auto-injected)

    Returns:
        Dictionary with posts and metadata
    """
    # Phase 1: Context accepted but not used yet
    # Phase 2+ will add: ctx.report_progress(), ctx.info(), etc.

    try:
        subreddit = reddit.subreddit(subreddit_name)

        # Get posts based on sort method
        if sort == "hot":
            posts = list(subreddit.hot(limit=limit))
        elif sort == "new":
            posts = list(subreddit.new(limit=limit))
        elif sort == "top":
            posts = list(subreddit.top(time_filter=time_filter, limit=limit))
        elif sort == "rising":
            posts = list(subreddit.rising(limit=limit))
        else:
            raise ValueError(f"Invalid sort method: {sort}")

        return {
            "success": True,
            "subreddit": subreddit_name,
            "posts": [format_post(p) for p in posts],
            "count": len(posts)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "subreddit": subreddit_name
        }
```

**Key observations:**
1. Only the function signature changed
2. Type hint added to docstring
3. No logic changes - context not used yet
4. Comment indicates Phase 1 status
