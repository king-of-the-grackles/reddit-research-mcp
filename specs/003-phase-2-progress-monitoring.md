# Phase 2: Progress Monitoring Implementation

**Status:** Ready for Implementation
**Created:** 2025-10-02
**Owner:** Engineering Team
**Depends On:** Phase 1 (Context Integration) ✅ Complete

## Executive Summary

This specification details Phase 2 of the FastMCP Context API integration: adding real-time progress reporting to long-running Reddit operations. With Phase 1 complete (all tools accept `Context`), this phase focuses on implementing `ctx.report_progress()` calls to provide visibility into multi-step operations.

**Timeline:** 1-2 days
**Effort:** Low (foundation already in place from Phase 1)

## Background

### Phase 1 Completion Summary

Phase 1 successfully integrated the FastMCP `Context` parameter into all tool and operation functions:
- ✅ All MCP tool functions accept `ctx: Context`
- ✅ All operation functions accept and receive context
- ✅ Helper functions updated with context forwarding
- ✅ 15 tests passing (8 integration tests + 7 updated existing tests)

**Current State:** Context is available but unused (commented as "Phase 1: Accept context but don't use it yet")

### Why Progress Monitoring?

Reddit operations can be time-consuming:
- **Vector search**: Searching thousands of subreddits and calculating confidence scores
- **Multi-subreddit fetches**: Fetching posts from 5-10 communities sequentially
- **Comment tree loading**: Parsing nested comment threads with hundreds of replies

Progress monitoring provides:
- Real-time feedback to users during long operations
- Prevention of timeout errors by showing active progress
- Better debugging visibility into operation performance
- Enhanced user experience with progress indicators

## Goals

1. ✅ Report progress during vector search iterations (`discover_subreddits`)
2. ✅ Report progress per subreddit in batch fetches (`fetch_multiple_subreddits`)
3. ✅ Report progress during comment tree traversal (`fetch_submission_with_comments`)
4. ✅ Maintain all existing test coverage (15 tests must pass)
5. ✅ Follow FastMCP progress reporting patterns from official docs

## Non-Goals

- Frontend progress UI (separate project)
- Progress for single-subreddit fetches (too fast to matter)
- Structured logging (Phase 3)
- Enhanced error handling (Phase 4)

## Implementation Plan

### Operation 1: discover_subreddits Progress

**File:** `src/tools/discover.py`
**Function:** `_search_vector_db()` (lines 101-239)
**Location:** Result processing loop (lines 137-188)

#### Current Code Pattern

```python
# Process results
processed_results = []
nsfw_filtered = 0

for metadata, distance in zip(
    results['metadatas'][0],
    results['distances'][0]
):
    # Skip NSFW if not requested
    if metadata.get('nsfw', False) and not include_nsfw:
        nsfw_filtered += 1
        continue

    # Calculate confidence score...
    # Apply penalties...
    # Determine match type...

    processed_results.append({...})
```

#### Enhanced Implementation

```python
# Process results
processed_results = []
nsfw_filtered = 0
total_results = len(results['metadatas'][0])

for i, (metadata, distance) in enumerate(zip(
    results['metadatas'][0],
    results['distances'][0]
)):
    # Report progress (async call required)
    if ctx:
        await ctx.report_progress(
            progress=i + 1,
            total=total_results,
            message=f"Analyzing r/{metadata.get('name', 'unknown')}"
        )

    # Skip NSFW if not requested
    if metadata.get('nsfw', False) and not include_nsfw:
        nsfw_filtered += 1
        continue

    # Calculate confidence score...
    # Apply penalties...
    # Determine match type...

    processed_results.append({...})
```

#### Changes Required

1. **Make function async**: Change `def _search_vector_db(...)` → `async def _search_vector_db(...)`
2. **Make parent function async**: Change `def discover_subreddits(...)` → `async def discover_subreddits(...)`
3. **Add await to calls**: Update `discover_subreddits` to `await _search_vector_db(...)`
4. **Add progress in loop**: Insert `await ctx.report_progress(...)` before processing each result
5. **Calculate total**: Add `total_results = len(results['metadatas'][0])` before loop

**Progress Events:** ~10-100 (depending on limit parameter)

---

### Operation 2: fetch_multiple_subreddits Progress

**File:** `src/tools/posts.py`
**Function:** `fetch_multiple_subreddits()` (lines 102-188)
**Location:** Subreddit iteration loop (lines 153-172)

#### Current Code Pattern

```python
# Parse posts and group by subreddit
posts_by_subreddit = {}
for submission in submissions:
    subreddit_name = submission.subreddit.display_name

    if subreddit_name not in posts_by_subreddit:
        posts_by_subreddit[subreddit_name] = []

    # Only add up to limit_per_subreddit posts per subreddit
    if len(posts_by_subreddit[subreddit_name]) < limit_per_subreddit:
        posts_by_subreddit[subreddit_name].append({...})
```

#### Enhanced Implementation

```python
# Parse posts and group by subreddit
posts_by_subreddit = {}
processed_subreddits = set()

for i, submission in enumerate(submissions):
    subreddit_name = submission.subreddit.display_name

    # Report progress when encountering a new subreddit
    if subreddit_name not in processed_subreddits:
        processed_subreddits.add(subreddit_name)
        if ctx:
            await ctx.report_progress(
                progress=len(processed_subreddits),
                total=len(subreddit_names),
                message=f"Fetching r/{subreddit_name}"
            )

    if subreddit_name not in posts_by_subreddit:
        posts_by_subreddit[subreddit_name] = []

    # Only add up to limit_per_subreddit posts per subreddit
    if len(posts_by_subreddit[subreddit_name]) < limit_per_subreddit:
        posts_by_subreddit[subreddit_name].append({...})
```

#### Changes Required

1. **Make function async**: Change `def fetch_multiple_subreddits(...)` → `async def fetch_multiple_subreddits(...)`
2. **Track processed subreddits**: Add `processed_subreddits = set()` before loop
3. **Add progress on new subreddit**: When a new subreddit is encountered, report progress
4. **Update server.py**: Add `await` when calling this function in `execute_operation()`

**Progress Events:** 1-10 (one per unique subreddit found)

---

### Operation 3: fetch_submission_with_comments Progress

**File:** `src/tools/comments.py`
**Function:** `fetch_submission_with_comments()` (lines 47-147)
**Location:** Comment parsing loop (lines 116-136)

#### Current Code Pattern

```python
# Parse comments
comments = []
comment_count = 0

for top_level_comment in submission.comments:
    if hasattr(top_level_comment, 'id') and hasattr(top_level_comment, 'body'):
        if comment_count >= comment_limit:
            break
        if isinstance(top_level_comment, PrawComment):
            comments.append(parse_comment_tree(top_level_comment, ctx=ctx))
        else:
            # Handle mock objects in tests
            comments.append(Comment(...))
        # Count all comments including replies
        comment_count += 1 + count_replies(comments[-1])
```

#### Enhanced Implementation

```python
# Parse comments
comments = []
comment_count = 0

for top_level_comment in submission.comments:
    if hasattr(top_level_comment, 'id') and hasattr(top_level_comment, 'body'):
        if comment_count >= comment_limit:
            break

        # Report progress before processing comment
        if ctx:
            await ctx.report_progress(
                progress=comment_count,
                total=comment_limit,
                message=f"Loading comments ({comment_count}/{comment_limit})"
            )

        if isinstance(top_level_comment, PrawComment):
            comments.append(parse_comment_tree(top_level_comment, ctx=ctx))
        else:
            # Handle mock objects in tests
            comments.append(Comment(...))
        # Count all comments including replies
        comment_count += 1 + count_replies(comments[-1])

# Report final completion
if ctx:
    await ctx.report_progress(
        progress=comment_count,
        total=comment_limit,
        message=f"Completed: {comment_count} comments loaded"
    )
```

#### Changes Required

1. **Make function async**: Change `def fetch_submission_with_comments(...)` → `async def fetch_submission_with_comments(...)`
2. **Add progress in loop**: Insert `await ctx.report_progress(...)` before parsing each top-level comment
3. **Add completion progress**: Report final progress after loop completes
4. **Update server.py**: Add `await` when calling this function in `execute_operation()`

**Progress Events:** ~5-100 (depending on comment_limit and tree depth)

---

## FastMCP Progress Patterns

### Basic Pattern (from FastMCP docs)

```python
from fastmcp import FastMCP, Context

@mcp.tool
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process a list of items with progress updates."""
    total = len(items)
    results = []

    for i, item in enumerate(items):
        # Report progress as we process each item
        await ctx.report_progress(progress=i, total=total)

        results.append(item.upper())

    # Report 100% completion
    await ctx.report_progress(progress=total, total=total)

    return {"processed": len(results), "results": results}
```

### Key Requirements

1. **Functions must be async** to use `await ctx.report_progress()`
2. **Progress parameter**: Current progress value (e.g., 5, 24, 0.75)
3. **Total parameter**: Optional total value (enables percentage calculation)
4. **Message parameter**: Optional descriptive message (not shown in examples above but supported)

### Best Practices

- Report at regular intervals (every iteration for small loops)
- Provide descriptive messages when possible
- Report final completion (100%)
- Don't spam - limit to reasonable frequency (5-10 events minimum)

## Testing Requirements

### Update Existing Tests

**File:** `tests/test_context_integration.py`

Add assertions to verify progress calls:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

class TestDiscoverSubredditsProgress:
    """Test progress reporting in discover_subreddits."""

    @pytest.mark.asyncio
    async def test_reports_progress_during_search(self, mock_context):
        """Verify progress is reported during vector search."""
        # Mock ChromaDB response with 3 results
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'Python', 'subscribers': 1000000, 'nsfw': False},
                {'name': 'learnpython', 'subscribers': 500000, 'nsfw': False},
                {'name': 'pythontips', 'subscribers': 100000, 'nsfw': False}
            ]],
            'distances': [[0.5, 0.7, 0.9]]
        }

        # Setup async mock for progress
        mock_context.report_progress = AsyncMock()

        with patch('src.tools.discover.get_chroma_client'), \
             patch('src.tools.discover.get_collection', return_value=mock_collection):

            result = await discover_subreddits(query="python", ctx=mock_context)

        # Verify progress was reported at least 3 times (once per result)
        assert mock_context.report_progress.call_count >= 3

        # Verify progress parameters
        first_call = mock_context.report_progress.call_args_list[0]
        assert 'progress' in first_call[1] or len(first_call[0]) >= 1
        assert 'total' in first_call[1] or len(first_call[0]) >= 2
```

### New Test Coverage

Add similar tests for:
- `test_fetch_multiple_subreddits_progress` - Verify progress per subreddit
- `test_fetch_comments_progress` - Verify progress during comment loading

### Success Criteria

- ✅ All existing 15 tests still pass
- ✅ New progress assertion tests pass
- ✅ Progress called at least 5 times per operation (varies by data)
- ✅ No performance degradation (progress overhead <5%)

## Server.py Updates

**File:** `src/server.py`
**Functions:** Update calls to async operations

### Current Pattern

```python
@mcp.tool
def execute_operation(
    operation_id: str,
    parameters: dict,
    ctx: Context
) -> dict:
    """Execute a Reddit operation by ID."""

    if operation_id == "discover_subreddits":
        return discover_subreddits(**params)
```

### Updated Pattern

```python
@mcp.tool
async def execute_operation(
    operation_id: str,
    parameters: dict,
    ctx: Context
) -> dict:
    """Execute a Reddit operation by ID."""

    if operation_id == "discover_subreddits":
        return await discover_subreddits(**params)
```

### Changes Required

1. **Make execute_operation async**: `async def execute_operation(...)`
2. **Add await to async operations**:
   - `await discover_subreddits(**params)`
   - `await fetch_multiple_subreddits(**params)`
   - `await fetch_submission_with_comments(**params)`

## Implementation Checklist

### Code Changes

- [ ] **src/tools/discover.py**
  - [ ] Make `discover_subreddits()` async
  - [ ] Make `_search_vector_db()` async
  - [ ] Add `await` to `_search_vector_db()` call
  - [ ] Add progress reporting in result processing loop
  - [ ] Calculate total before loop starts

- [ ] **src/tools/posts.py**
  - [ ] Make `fetch_multiple_subreddits()` async
  - [ ] Add `processed_subreddits` tracking set
  - [ ] Add progress reporting when new subreddit encountered

- [ ] **src/tools/comments.py**
  - [ ] Make `fetch_submission_with_comments()` async
  - [ ] Add progress reporting in comment parsing loop
  - [ ] Add final completion progress report

- [ ] **src/server.py**
  - [ ] Make `execute_operation()` async
  - [ ] Add `await` to `discover_subreddits()` call
  - [ ] Add `await` to `fetch_multiple_subreddits()` call
  - [ ] Add `await` to `fetch_submission_with_comments()` call

### Testing

- [ ] Update `tests/test_context_integration.py`
  - [ ] Add progress test for `discover_subreddits`
  - [ ] Add progress test for `fetch_multiple_subreddits`
  - [ ] Add progress test for `fetch_submission_with_comments`

- [ ] Run full test suite: `pytest tests/`
  - [ ] All 15 existing tests pass
  - [ ] New progress tests pass
  - [ ] No regressions

### Validation

- [ ] Manual testing with MCP Inspector or Claude Desktop
- [ ] Verify progress events appear in client logs
- [ ] Confirm no performance degradation
- [ ] Check that messages are descriptive and useful

## File Summary

### Files to Modify (4 files)

1. `src/tools/discover.py` - Add progress to vector search
2. `src/tools/posts.py` - Add progress to batch fetches
3. `src/tools/comments.py` - Add progress to comment loading
4. `src/server.py` - Make execute_operation async + await calls

### Files to Update (1 file)

1. `tests/test_context_integration.py` - Add progress assertions

### Files Not Modified

- `src/config.py` - No changes needed
- `src/models.py` - No changes needed
- `src/chroma_client.py` - No changes needed
- `src/resources.py` - No changes needed
- `tests/test_tools.py` - No changes needed (already passing)

## Success Criteria

### Functional Requirements

- ✅ Progress events emitted during vector search (≥5 per search)
- ✅ Progress events emitted during multi-subreddit fetch (1 per subreddit)
- ✅ Progress events emitted during comment loading (≥5 per fetch)
- ✅ Progress includes total when known
- ✅ Progress messages are descriptive

### Technical Requirements

- ✅ All functions properly async/await
- ✅ All 15+ tests pass
- ✅ No breaking changes to API
- ✅ Type hints maintained
- ✅ No performance degradation

### Quality Requirements

- ✅ Progress messages are user-friendly
- ✅ Progress updates at reasonable frequency (not spammy)
- ✅ Code follows FastMCP patterns from official docs
- ✅ Maintains consistency with Phase 1 implementation

## Estimated Effort

**Total Time:** 1-2 days

**Breakdown:**
- Code implementation: 3-4 hours
- Testing updates: 2-3 hours
- Manual validation: 1 hour
- Bug fixes & refinement: 1-2 hours

**Reduced from master spec (3-4 days)** because:
- Phase 1 foundation complete (Context integration done)
- Clear patterns established in codebase
- Limited scope (3 operations only)
- Existing test infrastructure in place

## Next Steps

After Phase 2 completion:
- **Phase 3**: Structured Logging (2-3 days)
- **Phase 4**: Enhanced Error Handling (2 days)
- **Phase 5**: Testing & Validation (1 day)

## References

- [FastMCP Progress Documentation](../ai-docs/fastmcp/docs/servers/progress.mdx)
- [FastMCP Context API](../ai-docs/fastmcp/docs/servers/context.mdx)
- [Phase 1 Completion Summary](./003-phase-1-context-integration.md) *(if created)*
- [Master Specification](./003-fastmcp-context-integration.md)
- Current Implementation: `src/server.py`, `src/tools/*.py`
