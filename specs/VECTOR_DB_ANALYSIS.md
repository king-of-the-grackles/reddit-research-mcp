# Reddit MCP Server - Vector Database Integration Analysis

## Executive Summary

The Reddit Research MCP server uses a **proxy-based ChromaDB integration** to provide semantic search across 20,000+ indexed subreddits. The vector database is abstracted behind a minimal HTTP proxy, allowing the server to work without exposing production credentials while maintaining full query capabilities.

**Current Status**: Phase 1 implementation with context integration foundation. Vector DB capabilities are actively used but only partially exposed.

---

## 1. Architecture Overview

### High-Level Stack

```
Frontend Request
    ↓
MCP Server (FastMCP)
    ↓
discover_subreddits() tool
    ↓
chroma_client.py (ChromaProxyClient)
    ↓
CHROMA_PROXY_URL HTTP Endpoint
    ↓
ChromaDB Cloud Instance (Private)
    ↓
Embedded Vectors (Subreddit embeddings)
```

### Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **ChromaProxyClient** | `src/chroma_client.py:16-84` | HTTP proxy client that mimics ChromaDB interface |
| **ProxyCollection** | `src/chroma_client.py:72-83` | Wrapper matching ChromaDB collection interface |
| **discover_subreddits()** | `src/tools/discover.py:10-98` | Main entry point for subreddit discovery |
| **_search_vector_db()** | `src/tools/discover.py:101-248` | Internal semantic search implementation |
| **validate_subreddit()** | `src/tools/discover.py:251-310` | Exact match validation in vector DB |
| **Proxy Server** | Private repo on Render | HTTP endpoint at `https://reddit-mcp-vector-db.onrender.com` |

---

## 2. Vector Database Client Implementation

### ChromaProxyClient Class

**File**: `/src/chroma_client.py:16-84`

```python
class ChromaProxyClient:
    """Proxy client that mimics ChromaDB interface."""
    
    def __init__(self, proxy_url: Optional[str] = None):
        self.url = proxy_url or os.getenv(
            'CHROMA_PROXY_URL', 
            'https://reddit-mcp-vector-db.onrender.com'
        )
        self.api_key = os.getenv('CHROMA_PROXY_API_KEY')
        self.session = requests.Session()
        if self.api_key:
            self.session.headers['X-API-Key'] = self.api_key
```

**Key Features**:
- Minimal implementation (~70 lines)
- Uses `requests` library for HTTP communication
- Supports optional API key authentication via headers
- Singleton pattern with module-level caching
- Error handling for auth (401), permissions (403), rate limits (429)

**Available Methods**:
1. `query(query_texts: List[str], n_results: int = 10)` - Semantic search
2. `list_collections()` - Returns hardcoded `["reddit_subreddits"]`
3. `count()` - Attempts stats endpoint, defaults to 20000

### HTTP Interface

**Endpoint**: `https://reddit-mcp-vector-db.onrender.com`

**Implemented Routes**:

| Route | Method | Input | Output |
|-------|--------|-------|--------|
| `/query` | POST | `{"query_texts": [...], "n_results": int}` | ChromaDB result format |
| `/stats` | GET | None | `{"total_subreddits": int}` |

**Authentication**: Optional `X-API-Key` header (currently required in production)

### Error Handling

Graceful degradation with specific messages:
- **401**: "Authentication failed: API key required"
- **403**: "Authentication failed: Invalid API key"
- **429**: "Rate limit exceeded. Please wait before retrying"
- **Other HTTP errors**: Generic HTTP error message
- **Network errors**: Connection error message

---

## 3. discover_subreddits Operation - Complete Flow

### Entry Point Parameters

**File**: `src/tools/discover.py:10-98`

```python
async def discover_subreddits(
    query: Optional[str] = None,
    queries: Optional[Union[List[str], str]] = None,
    limit: int = 10,
    include_nsfw: bool = False,
    ctx: Context = None
) -> Dict[str, Any]
```

**Parameter Details**:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `query` | string | None | 2-100 chars | Single search term (mutually exclusive with `queries`) |
| `queries` | list\|string | None | N/A | Batch queries - can be list or JSON string |
| `limit` | int | 10 | 1-50 | Results per query (capped internally at 100) |
| `include_nsfw` | bool | False | N/A | Include NSFW subreddits |
| `ctx` | Context | None | N/A | FastMCP context for progress reporting |

**Batch Query Handling** (lines 52-83):
- Accepts list of strings: `["machine learning", "AI"]`
- Accepts JSON string: `'["term1", "term2"]'`
- Auto-detects and parses JSON format
- Returns dict with queries as keys, results as values
- Reports API calls made and tip about batch efficiency

### Internal Search Implementation

**File**: `src/tools/discover.py:101-248`

```
_search_vector_db():
1. Connect to vector DB (lines 111-112)
2. Validate connection (error handling)
3. Search with limit inflation (lines 113-118)
4. Get results from ChromaDB (lines 116-119)
5. Process & filter results (lines 134-197)
6. Sort by confidence & subscribers (lines 199-200)
7. Limit to requested number (line 203)
8. Calculate stats (lines 205-206)
9. Return formatted results (lines 215-224)
```

### Response Format

**Success Response**:
```json
{
  "query": "machine learning",
  "subreddits": [
    {
      "name": "MachineLearning",
      "subscribers": 1500000,
      "confidence": 0.95,
      "url": "https://reddit.com/r/MachineLearning"
    },
    // ... more results
  ],
  "summary": {
    "total_found": 142,
    "returned": 10,
    "has_more": true
  },
  "next_actions": ["142 total results found, showing 10"]
}
```

**Batch Mode Response**:
```json
{
  "batch_mode": true,
  "total_queries": 3,
  "api_calls_made": 3,
  "results": {
    "query1": { /* single query result */ },
    "query2": { /* single query result */ }
  },
  "tip": "Batch mode reduces API calls. Use the exact 'name' field..."
}
```

**Error Response**:
```json
{
  "error": "Failed to connect to vector database: [details]",
  "results": [],
  "summary": {
    "total_found": 0,
    "returned": 0,
    "coverage": "error"
  }
}
```

---

## 4. Vector Database Query Characteristics

### Semantic Search Behavior

**Query Process** (lines 116-119):
```python
search_limit = min(limit * 3, 100)  # Get extra for filtering
results = collection.query(
    query_texts=[query],
    n_results=search_limit
)
```

**Key Points**:
- Requests 3x desired limit to allow filtering without loss
- Caps at 100 results max (ChromaDB collection limitation)
- Returns metadata AND distance scores for ALL results
- Results ordered by distance (ascending - closer matches first)

### Distance Score Handling

**Observed Behavior**:
- Distance range: typically 0.8 to 1.6+ (Euclidean metric)
- Lower distance = higher semantic similarity
- Non-normalized (not 0-1 scale)

**Confidence Conversion** (lines 158-167):
```python
# Piecewise mapping of distance to confidence
if distance < 0.8:
    confidence = 0.9 + (0.1 * (0.8 - distance) / 0.8)  # 0.9-1.0
elif distance < 1.0:
    confidence = 0.7 + (0.2 * (1.0 - distance) / 0.2)  # 0.7-0.9
elif distance < 1.2:
    confidence = 0.5 + (0.2 * (1.2 - distance) / 0.2)  # 0.5-0.7
elif distance < 1.4:
    confidence = 0.3 + (0.2 * (1.4 - distance) / 0.2)  # 0.3-0.5
else:
    confidence = max(0.1, 0.3 * (2.0 - distance) / 0.6)  # 0.1-0.3
```

This is a **heuristic mapping**, not based on formal statistical significance.

### Post-Search Filtering & Ranking

**NSFW Filtering** (lines 151-153):
- Skip if `metadata.get('nsfw', False) and not include_nsfw`
- Count filtered results separately

**Match Type Classification** (lines 183-190):
```python
if distance < 0.3:
    match_type = "exact_match"
elif distance < 0.7:
    match_type = "strong_match"
elif distance < 1.0:
    match_type = "partial_match"
else:
    match_type = "weak_match"
```
*Note: `match_type` is computed but NOT returned in results*

**Generic Subreddit Penalty** (lines 170-173):
```python
generic_subs = ['funny', 'pics', 'videos', 'gifs', 'memes', 'aww']
if subreddit_name in generic_subs and query.lower() not in subreddit_name:
    confidence *= 0.3  # Heavy penalty (70% reduction)
```

**Subscriber-Based Adjustment** (lines 176-180):
- Very large (>1M): +10% boost (capped at 1.0)
- Very small (<10K): -10% penalty

**Final Sorting** (lines 199-200):
```python
processed_results.sort(key=lambda x: (-x['confidence'], -(x['subscribers'] or 0)))
```
Primary sort: confidence (highest first). Secondary: subscribers (highest first).

---

## 5. Available Metadata from Vector DB

### What ChromaDB Collection Contains

Based on code inspection, the `reddit_subreddits` collection stores:

**Per-Subreddit Metadata** (accessed via `metadata.get()`):
- `name` (str) - Subreddit name
- `subscribers` (int) - Current subscriber count
- `nsfw` (bool) - Is NSFW flag
- `url` (str) - Full URL to subreddit
- Plus likely: description, active status, etc.

**Per-Query Result**:
- `metadatas` - List of metadata dicts
- `distances` - List of distance scores (1:1 mapping)
- Implicitly: embeddings (not exposed to client)

### What's NOT Directly Exposed

From the codebase analysis:
- **Embedding vectors** - ChromaDB has them, but API doesn't return them
- **Distance scores** - Used internally for confidence calc, not returned
- **Match type** - Calculated but not included in results
- **Metadata completeness** - Unclear which fields always present
- **Embedding metadata** - How/when vectors were created
- **Collection stats** - Only count available via `/stats`
- **Search timing** - No latency metrics returned
- **Raw query distance** - No way to filter by distance threshold

---

## 6. validate_subreddit Helper

**File**: `src/tools/discover.py:251-310`

Purpose: Verify a subreddit exists in the indexed database

**Parameters**:
- `subreddit_name` (str) - Name to validate (handles r/ prefix)
- `ctx` (Context) - Optional FastMCP context

**Process**:
1. Clean name (remove r/ prefix)
2. Query vector DB with exact name
3. Search top 5 results for exact name match
4. Return validation result

**Response Format**:
```json
{
  "valid": true,
  "name": "MachineLearning",
  "subscribers": 1500000,
  "is_private": false,
  "over_18": false,
  "indexed": true
}
```

**Limitations**:
- Only checks if name exists in vector DB index
- Does NOT validate against live Reddit API
- Assumes all indexed subreddits are public (hardcoded)

---

## 7. Vector DB Integration Points in Other Operations

### search_subreddit (Search within subreddit)
**File**: `src/tools/search.py:8-84`
- **Does NOT use vector DB**
- Uses Reddit API directly with `subreddit.search()`
- Could benefit from vector search for conceptual queries

### fetch_subreddit_posts
**File**: `src/tools/posts.py:8-99`
- **Does NOT use vector DB**
- Fetches posts from known subreddit via Reddit API
- Called AFTER discover_subreddits identifies communities

### fetch_multiple_subreddits
**File**: `src/tools/posts.py:102-200`
- **Does NOT use vector DB**
- Batch fetches from list of subreddit names
- Input: list of exact names (from discover_subreddits)

### fetch_submission_with_comments
**File**: `src/tools/comments.py:47-164`
- **Does NOT use vector DB**
- Fetches comment tree for specific post
- Input: submission ID or URL (from fetch operations)

### Pattern: Vector DB → Reddit API Pipeline
```
discover_subreddits (USES VECTOR DB)
    ↓ (returns subreddit names)
fetch_multiple_subreddits (uses Reddit API)
    ↓ (returns post IDs)
fetch_submission_with_comments (uses Reddit API)
    ↓ (returns full discussion tree)
```

---

## 8. MCP Server Integration - Three-Layer Architecture

**File**: `src/server.py:140-429`

### Layer 1: discover_operations() (Lines 142-171)
- Lists available operations (5 total)
- Shows recommended workflows
- No parameters required

### Layer 2: get_operation_schema() (Lines 174-372)
- Provides parameter requirements
- Includes validation rules and examples
- For `discover_subreddits`:
  - Parameters: `query`, `limit`, `include_nsfw`
  - Returns: array with confidence scores

### Layer 3: execute_operation() (Lines 375-428)
- Actually executes the operation
- Maps operation IDs to functions
- For `discover_subreddits`: calls `discover_subreddits(query, limit, include_nsfw, ctx)`

---

## 9. Current Capabilities - What's Exposed

### Parameters Supported

**discover_subreddits**:
- [x] Single query (`query` parameter)
- [x] Batch queries (`queries` parameter)
- [x] Result limit (`limit` parameter, 1-50)
- [x] NSFW filtering (`include_nsfw` boolean)
- [x] Progress reporting (via `ctx`)

### Data Returned

Per subreddit result:
- [x] Subreddit name
- [x] Subscriber count
- [x] Confidence score (0.0-1.0)
- [x] URL
- [ ] Distance score
- [ ] Match type classification
- [ ] Metadata completeness indicator
- [ ] Last updated timestamp

Per query:
- [x] Query string echo
- [x] Array of results
- [x] Summary (total found, returned, has_more)
- [x] Next actions (suggestions)
- [ ] Search statistics
- [ ] Execution time
- [ ] Result quality metrics

### Vector DB Capabilities Used

- [x] Semantic similarity search
- [x] Top-K result retrieval
- [x] Distance score generation
- [x] NSFW metadata filtering
- [x] Metadata access
- [x] Collection counting
- [ ] Metadata filtering/where clauses
- [ ] Hybrid search (text + semantic)
- [ ] Embedding search (vector input)
- [ ] Collection statistics
- [ ] Advanced analytics
- [ ] Aggregation queries

---

## 10. Vector DB Capabilities NOT Currently Exposed

### High-Value Opportunities

| Capability | Impact | Effort | Details |
|-----------|--------|--------|---------|
| **Distance thresholds** | High | Low | Filter results by confidence/distance range |
| **Result clustering** | High | Medium | Group similar results, show diversity |
| **Metadata filters** | High | Medium | Filter by subscriber range, language, etc. |
| **Recommendation** | High | Medium | "Similar communities to this one" |
| **Temporal analysis** | Medium | High | Growth trends, activity changes |
| **Quality scores** | Medium | Low | Combine multiple signals (distance, activity) |
| **Batch similarity** | Medium | Low | Compare multiple queries for overlap |
| **Result dedup** | Low | Low | Remove near-duplicates from batch |

### Low-Value Opportunities

- Raw embedding vectors (no use case without special client)
- Full metadata dump (data leak risk)
- Collection rebuild triggers (operational only)
- Advanced analytics (expensive, slow)

---

## 11. Confidence Calculation Deep Dive

### Current Algorithm

The confidence score is NOT based on:
- Statistical significance testing
- Cross-validation metrics
- Training set performance
- Any formal ML evaluation

It IS:
- A heuristic mapping of distance to 0-1 range
- Calibrated by observed distance distributions
- Post-processed with business rules

### Piecewise Linear Mapping

Distance ranges and confidence mapping:

```
Distance    Confidence Range
0.0-0.8     0.9-1.0      (excellent match)
0.8-1.0     0.7-0.9      (very good)
1.0-1.2     0.5-0.7      (good)
1.2-1.4     0.3-0.5      (fair)
1.4-2.0     0.1-0.3      (weak)
2.0+        0.1          (very weak)
```

### Adjustments Applied (in order)

1. **Distance → base confidence** (piecewise linear, lines 158-167)
2. **Generic subreddit penalty** (×0.3 if generic and not directly searched, lines 170-173)
3. **Large subreddit boost** (×1.1 if >1M subscribers, lines 177-178)
4. **Small subreddit penalty** (×0.9 if <10K subscribers, lines 179-180)

### Example Calculation

Query: "machine learning"
Returned result: r/funny with distance=0.95

1. Base confidence: 0.7 + (0.2 * (1.0 - 0.95) / 0.2) = 0.75
2. Generic penalty: 0.75 * 0.3 = 0.225
3. Final: 0.225 → rounds to 0.225 (≈ weak match)

---

## 12. Error Recovery & Guidance

**File**: `src/tools/discover.py:227-248`

Built-in error pattern matching:

```python
error_str = str(e).lower()
if "not found" in error_str:
    guidance = "Verify subreddit name spelling"
elif "rate" in error_str:
    guidance = "Rate limited - wait 60 seconds"
elif "timeout" in error_str:
    guidance = "Reduce limit parameter to 10"
else:
    guidance = "Try simpler search terms"
```

---

## 13. Collection Schema (Inferred)

### reddit_subreddits Collection

**Embedding**: Presumably multi-field embedding of:
- Subreddit name
- Description
- Community focus/purpose
- (Possibly) recent posts/activity

**Metadata Fields**:
- `name` (str, required) - Subreddit name
- `subscribers` (int) - Subscriber count
- `nsfw` (bool) - Adult content flag
- `url` (str) - Reddit URL
- Possibly: `description`, `active`, `created`, `language`

**Index Size**: ~20,000 subreddits
**Vector Dimension**: Unknown (ChromaDB uses embeddings, likely 384-1536)
**Update Frequency**: Unknown (static for MVP)

---

## 14. Performance Characteristics

### Query Performance

**Observed**:
- Typical response: <2 seconds (proxy latency + network)
- Search limit: 100 max results
- Batch overhead: Minimal (sequential API calls)

**Bottlenecks**:
- Network latency to proxy endpoint
- Network latency from proxy to ChromaDB Cloud
- ChromaDB search time (typically <100ms for 20K collection)
- Confidence calculation (linear O(n), minimal)
- Sorting (O(n log n), minimal)

### Scaling Limits

- Max per-query results: 100 (ChromaDB limit)
- Batch query limit: Untested (probably ~10-20 practical)
- Concurrent requests: Depends on proxy service (Render free tier: ~10)

---

## 15. Code Locations Reference

### Main Files

| File | Lines | Purpose |
|------|-------|---------|
| `src/chroma_client.py` | 164 | ChromaDB proxy client |
| `src/tools/discover.py` | 310 | Subreddit discovery |
| `src/models.py` | 60 | Data models |
| `src/server.py` | 607 | MCP server & operations |
| `src/config.py` | 46 | Reddit client config |
| `src/resources.py` | 212 | Server info resource |

### Key Functions

| Function | File | Lines | Purpose |
|----------|------|-------|---------|
| `get_chroma_client()` | chroma_client.py | 89-104 | Client initialization |
| `get_collection()` | chroma_client.py | 113-130 | Collection access |
| `test_connection()` | chroma_client.py | 133-164 | Connection test |
| `discover_subreddits()` | discover.py | 10-98 | Entry point |
| `_search_vector_db()` | discover.py | 101-248 | Search implementation |
| `validate_subreddit()` | discover.py | 251-310 | Validation helper |
| `execute_operation()` | server.py | 378-428 | Operation dispatcher |

---

## 16. Environment Configuration

**Environment Variables**:

```bash
# Vector Database Proxy
CHROMA_PROXY_URL=https://reddit-mcp-vector-db.onrender.com
CHROMA_PROXY_API_KEY=<optional-api-key>

# Reddit API (for other operations)
REDDIT_CLIENT_ID=<app-id>
REDDIT_CLIENT_SECRET=<app-secret>
REDDIT_USER_AGENT=RedditMCP/1.0  # optional, default provided
```

**Default Behaviors**:
- If `CHROMA_PROXY_URL` not set: Uses production Render URL
- If `CHROMA_PROXY_API_KEY` not set: Makes unauthenticated requests
- If both fail: Returns error with helpful guidance

---

## 17. Phase 1 Context Integration Status

**File**: `src/tools/discover.py:34, 109, 143-148`

Current implementation:
- [x] Accepts `ctx: Context` parameter
- [x] Uses `ctx.report_progress()` for streaming updates
- [x] Reports: progress number, total, message
- [ ] Does NOT use for filtering/ranking
- [ ] Does NOT use for caching
- [ ] Does NOT use for request tracking

**Lines with Context Usage**:
```python
# Line 143-148: Progress reporting
if ctx:
    await ctx.report_progress(
        progress=i + 1,
        total=total_results,
        message=f"Analyzing r/{metadata.get('name', 'unknown')}"
    )
```

---

## 18. Specific Recommendations for Enhancement

### Phase 2a: Low-Effort Confidence Improvements

1. **Expose raw distance scores**
   - Add `distance` field to returned results
   - Users can make their own confidence thresholds
   - ~2 lines of code change
   - File: `src/tools/discover.py:192-197`

2. **Add quality tier labels**
   - Return `match_tier` instead of just confidence
   - Calculated at line 183-190 already
   - ~3 lines change
   - File: `src/tools/discover.py:192-197`

3. **Expose filtering count**
   - Return `nsfw_filtered` count in summary
   - Variable already calculated at line 152
   - ~2 lines change
   - File: `src/tools/discover.py:215-224`

4. **Add result statistics**
   - Mean/median confidence in summary
   - Subscriber stats (min/max/median)
   - ~5 lines of code
   - File: `src/tools/discover.py:205-213`

### Phase 2b: Medium-Effort Vector DB Features

5. **Distance-based filtering**
   - Add parameter `min_confidence` (0.0-1.0)
   - Filter results before returning
   - Keep same code structure
   - ~10 lines of code
   - File: `src/tools/discover.py:150-203`

6. **Subscriber range filtering**
   - Add parameters `min_subscribers`, `max_subscribers`
   - Filter at lines 151-180
   - ~5 lines of code
   - File: `src/tools/discover.py:150-203`

7. **Match diversity**
   - Add parameter `diversity_mode` (balanced/focused/diverse)
   - Balanced: current behavior
   - Focused: only highest confidence
   - Diverse: spread across distance ranges
   - ~15 lines of code
   - File: `src/tools/discover.py:199-203`

### Phase 2c: Advanced Features

8. **Similar subreddits**
   - New operation: `find_similar_subreddits(subreddit_name, limit)`
   - Uses vector DB to find semantically similar communities
   - ~30 lines of code
   - File: new `src/tools/similarity.py`

9. **Batch query analysis**
   - In batch mode, analyze query term relationships
   - Show which queries have overlapping results
   - Show unique vs shared subreddits per query
   - ~40 lines of code
   - File: `src/tools/discover.py:67-83` expansion

10. **Collection introspection**
    - New operation: `analyze_collection_coverage(query)`
    - Show how many indexed subreddits match different confidence thresholds
    - Helps users understand search space
    - ~30 lines of code
    - File: new `src/tools/analytics.py`

---

## 19. Architecture Diagrams

### Request Flow

```
User Query
    ↓
execute_operation("discover_subreddits", {...})
    ↓
discover_subreddits(query, limit, include_nsfw, ctx)
    ↓
get_chroma_client() [cached]
    ↓
ChromaProxyClient(url="...onrender.com")
    ↓
HTTP POST /query
    ↓
Proxy Server (Render)
    ↓
ChromaDB Cloud Instance
    ↓
Vector Search (Euclidean)
    ↓
Returns: {
  "metadatas": [[{name, subscribers, nsfw, url}]],
  "distances": [[0.95, 1.05, ...]]
}
    ↓
_search_vector_db() processes:
  1. NSFW filter
  2. Distance → confidence
  3. Generic sub penalty
  4. Subscriber adjustment
  5. Sort by confidence & subscribers
  6. Limit to requested
    ↓
Return formatted results
```

### Data Flow - Batch Mode

```
Input: ["query1", "query2", "query3"]
    ↓
For each query:
    ↓
    _search_vector_db(query, ...)
    ↓ [progress update via ctx]
    ↓
    Process & return results
    ↓
Aggregate into batch response:
{
  "batch_mode": true,
  "total_queries": 3,
  "results": {
    "query1": {...},
    "query2": {...},
    "query3": {...}
  }
}
```

---

## 20. Testing & Validation Points

**Current Test Coverage**:
- Files: `tests/test_tools.py`, `tests/test_context_integration.py`
- Focus: Async/await patterns, context integration

**What Should Be Tested**:

| Component | Test Type | Coverage |
|-----------|-----------|----------|
| ChromaProxyClient | Unit | Connection, auth errors, timeouts |
| Distance→Confidence | Unit | All 5 piecewise ranges |
| NSFW filtering | Unit | Filtered vs unfiltered |
| Generic sub penalty | Unit | Penalty application |
| Batch processing | Integration | Multiple queries end-to-end |
| Error recovery | Integration | Each error type mapped |
| sorting logic | Unit | Confidence then subscribers |
| Validation (exact match) | Integration | Found vs not found |

---

## 21. Key Takeaways for Development

### What Works Well
1. **Minimal proxy abstraction** - Simple, maintainable HTTP layer
2. **Confidence scoring** - Practical heuristic for user guidance
3. **Batch efficiency** - Single API call per query, not per result
4. **Error handling** - Specific messages guide users
5. **Metadata-driven filtering** - No extra queries needed

### Pain Points
1. **Distance scores not exposed** - Users can't fine-tune thresholds
2. **No metadata filter API** - Can't search by subscriber range in vector DB
3. **Static confidence algorithm** - Doesn't improve with feedback
4. **No search analytics** - Can't see which queries work well
5. **Collection not updatable from server** - Would require separate pipeline

### Expansion Opportunities
1. **Filtered searches** - Add WHERE clause support to proxy
2. **Similarity searches** - Vector similarity between queries/subreddits
3. **Embedding export** - For advanced users/tools
4. **Analytics endpoint** - Collection statistics and trends
5. **Recommendation engine** - Based on user interaction patterns

---

## File Structure Summary

```
reddit-research-mcp/
├── src/
│   ├── __init__.py
│   ├── chroma_client.py        ← Vector DB client
│   ├── config.py               ← Reddit client config
│   ├── models.py               ← Data models
│   ├── server.py               ← MCP server & operations
│   ├── resources.py            ← Server info endpoint
│   └── tools/
│       ├── __init__.py
│       ├── discover.py         ← Vector DB queries
│       ├── search.py           ← Reddit API search
│       ├── posts.py            ← Reddit API posts
│       └── comments.py         ← Reddit API comments
├── specs/                       ← Architecture docs
├── tests/                       ← Test suite
└── README.md                    ← Project overview
```

All vector DB integration lives in 2 files:
- `src/chroma_client.py` (proxy client)
- `src/tools/discover.py` (discovery operations)

