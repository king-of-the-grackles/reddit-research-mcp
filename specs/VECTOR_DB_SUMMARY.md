# Reddit MCP Server - Vector DB Integration Summary

## Quick Reference

**File**: `/Users/chrisivester/Documents/mbp-obsidian-vault/02-Projects/software-projects/MCP/reddit-mcp-poc/reddit-research-mcp/VECTOR_DB_ANALYSIS.md` (21 detailed sections)

---

## Current State

### What It Does
- Semantic search across 20,000+ indexed subreddits via HTTP proxy
- Discovers relevant communities based on natural language queries
- Ranks results using confidence scores (0.0-1.0)
- Supports batch queries and NSFW filtering
- Integrates with FastMCP context for progress reporting

### How It Works

```
Query → ChromaProxyClient → HTTP Proxy (Render) → ChromaDB Cloud
                                                        ↓
                                          Vector Search (Euclidean)
                                                        ↓
                                    Returns distances + metadata
                                                        ↓
                    Process: Distance→Confidence, Filter, Sort
                                                        ↓
                              Return ranked subreddit list
```

### Key Components

| Component | Lines | Purpose |
|-----------|-------|---------|
| `ChromaProxyClient` | chroma_client.py:16-84 | HTTP proxy client |
| `discover_subreddits()` | discover.py:10-98 | Main entry point |
| `_search_vector_db()` | discover.py:101-248 | Search logic |
| `validate_subreddit()` | discover.py:251-310 | Exact match check |

---

## API Surface (What's Exposed)

### Parameters

```python
discover_subreddits(
    query: str = None,           # Single search term
    queries: List[str] = None,   # Batch queries (mutually exclusive)
    limit: int = 10,             # Results per query (1-50)
    include_nsfw: bool = False,  # Include adult content
    ctx: Context = None          # Progress reporting
)
```

### Return Values

**Per Subreddit**:
- `name` - Subreddit name
- `subscribers` - Subscriber count
- `confidence` - Match score (0.0-1.0)
- `url` - Reddit URL

**Per Query**:
- `query` - Query echo
- `subreddits` - Array of results
- `summary.total_found` - Total matches
- `summary.returned` - Results shown
- `summary.has_more` - More available
- `next_actions` - Suggestions

---

## What Vector DB Provides vs What's Exposed

### Currently Used
- [x] Semantic similarity search (via distance)
- [x] Top-K retrieval (up to 100)
- [x] Distance scores
- [x] Metadata (name, subscribers, nsfw, url)
- [x] Collection counting

### Currently NOT Exposed
- [ ] Raw distance scores
- [ ] Match type classifications
- [ ] Metadata filtering (WHERE clauses)
- [ ] Embedding vectors
- [ ] Search latency/timing
- [ ] Collection statistics
- [ ] Advanced filtering options

---

## Confidence Score Deep Dive

### NOT Based On
- Statistical significance
- Cross-validation metrics
- Any formal ML evaluation

### IS Based On
- Heuristic distance→confidence mapping
- Observed distance distribution (0.8-1.6+ range)
- Business rules (penalties/boosts)

### Mapping Formula

```python
# Piecewise linear conversion
distance < 0.8   → confidence 0.9-1.0  (excellent)
distance < 1.0   → confidence 0.7-0.9  (very good)
distance < 1.2   → confidence 0.5-0.7  (good)
distance < 1.4   → confidence 0.3-0.5  (fair)
distance ≥ 1.4   → confidence 0.1-0.3  (weak)

# Then apply adjustments:
- Generic subs penalty: ×0.3 (if 'funny', 'pics', etc.)
- Large subs boost: ×1.1 (if >1M subscribers)
- Small subs penalty: ×0.9 (if <10K subscribers)
```

---

## Environment Setup

```bash
# Required
REDDIT_CLIENT_ID=<your-id>
REDDIT_CLIENT_SECRET=<your-secret>

# Optional (defaults provided)
CHROMA_PROXY_URL=https://reddit-mcp-vector-db.onrender.com
CHROMA_PROXY_API_KEY=<optional>
REDDIT_USER_AGENT=RedditMCP/1.0
```

---

## Enhancement Roadmap

### Phase 2a: Quick Wins (1-2 hours each)
1. Expose raw distance scores
2. Return match tier labels (exact/strong/partial/weak)
3. Include NSFW filter count in summary
4. Add confidence statistics (mean/median)

### Phase 2b: Medium Features (3-4 hours each)
5. Add `min_confidence` filter parameter
6. Add subscriber range filters
7. Add result diversity modes (focused/balanced/diverse)

### Phase 2c: Advanced Features (6+ hours each)
8. Similar subreddits operation
9. Batch query overlap analysis
10. Collection coverage analysis

---

## Code Quality Checklist

- [x] ChromaProxyClient is minimal (~70 lines) and maintainable
- [x] Error handling with specific guidance
- [x] Batch mode support
- [x] Progress reporting integration
- [x] Metadata-driven filtering (no extra queries)
- [ ] Distance scores exposed to users
- [ ] No architectural debt
- [ ] Test coverage for distance→confidence
- [ ] Test coverage for filtering logic

---

## Testing Strategy

**Unit Tests Needed**:
- Distance→Confidence conversion (all 5 ranges)
- Generic subreddit penalty application
- Subscriber-based adjustments
- NSFW filtering behavior

**Integration Tests Needed**:
- Single query end-to-end
- Batch query execution
- Error recovery paths
- Exact match validation

---

## Known Limitations

1. **Distance not exposed** - Users can't set custom thresholds
2. **No WHERE clause support** - Can't filter by subscriber range in DB
3. **Static confidence algorithm** - No learning from feedback
4. **Collection not updatable** - Would need separate pipeline
5. **Batch limit untested** - Probably ~10-20 queries max

---

## Performance Notes

- Typical response: <2 seconds (network + search + processing)
- Search limit: 100 results max
- Batch overhead: Minimal (sequential calls, not parallel)
- Bottlenecks: Network latency, not compute

---

## Context Integration Status

**Current** (Phase 1):
- [x] Accepts `ctx: Context` parameter
- [x] Uses `ctx.report_progress()` for streaming
- [x] Reports progress during filtering

**Not Yet Used**:
- Filtering/ranking decisions
- Caching of results
- Request tracking
- Analytics collection

---

## Key Files

```
reddit-research-mcp/src/
├── chroma_client.py      ← Vector DB proxy (164 lines)
├── tools/discover.py     ← Discovery operations (310 lines)
├── server.py             ← MCP operations dispatcher
├── models.py             ← Data structures
└── config.py             ← Reddit API setup
```

**All vector DB integration in 2 files:**
- `chroma_client.py` (70 lines of actual logic)
- `discover.py` (150 lines for search + validation)

---

## For Phase 2a/2b/2c Development

### Starting Point
1. Read VECTOR_DB_ANALYSIS.md (full details)
2. Review Section 18 (Enhancement Roadmap)
3. Check specific file lines for modifications
4. Run existing tests to ensure baseline

### Making Changes
1. Add parameters to `discover_subreddits()` signature
2. Update schema in `server.py:get_operation_schema()`
3. Implement filtering logic in `_search_vector_db()`
4. Add tests for new features
5. Update docstrings

### Testing
- Mock ChromaDB responses
- Test confidence calculations
- Test filter combinations
- Test error cases

---

## Questions This Analysis Answers

✓ How is the vector DB integrated?
✓ What parameters does discover_subreddits accept?
✓ What data is currently returned?
✓ How are distance scores converted to confidence?
✓ What Vector DB capabilities exist but aren't exposed?
✓ Where should new features be added?
✓ What's the performance impact?
✓ How does context integration work?
✓ What are good next features to build?
✓ How is error handling implemented?

