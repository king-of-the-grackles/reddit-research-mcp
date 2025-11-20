# Comprehensive Guide: Subreddit Discovery Tools for LLM Agents

This guide documents the subreddit discovery tools and best practices for LLM agents using the Reddit Research MCP server.

**Target Audience:** LLM agents using the MCP server via the three-layer architecture (discover_operations → get_operation_schema → execute_operation)

---

## 1. Tool API Reference

### Primary Tool: `discover_subreddits`

**Purpose:** Find relevant Reddit communities using semantic vector search across 20,000+ indexed subreddits.

#### Function Signature

```python
async def discover_subreddits(
    query: Optional[str] = None,
    queries: Optional[Union[List[str], str]] = None,
    limit: int = 10,
    include_nsfw: bool = False,
    min_confidence: float = 0.0,
    ctx: Context = None
) -> Dict[str, Any]
```

#### Parameters (LLM-Accessible via MCP)

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `query` | string | None | 2-100 chars | Single search topic. Required if `queries` not provided |
| `queries` | array[string] or JSON string | None | N/A | Multiple topics for batch discovery. More efficient than single queries. Can be array or JSON string like `'["term1", "term2"]'` |
| `limit` | integer | 10 | 1-50 | Number of results per query |
| `include_nsfw` | boolean | False | N/A | Include NSFW communities in results |
| `min_confidence` | float | 0.0 | 0.0-1.0 | Filter results: only return subreddits with confidence ≥ this value |

#### Return Structure: Single Query Mode

```json
{
  "query": "search term",
  "subreddits": [
    {
      "name": "subreddit_name",
      "subscribers": 150000,
      "confidence": 0.85,
      "distance": 0.45,
      "match_tier": "semantic",
      "url": "https://reddit.com/r/subreddit_name"
    }
  ],
  "summary": {
    "total_found": 25,
    "returned": 10,
    "has_more": true,
    "confidence_stats": {
      "mean": 0.78,
      "median": 0.82,
      "min": 0.65,
      "max": 0.92,
      "std_dev": 0.08
    },
    "tier_distribution": {
      "exact": 3,
      "semantic": 5,
      "adjacent": 2,
      "peripheral": 0
    }
  },
  "next_actions": [
    "25 total results found, showing 10",
    "3 NSFW subreddits filtered"
  ]
}
```

#### Return Structure: Batch Query Mode

```json
{
  "batch_mode": true,
  "total_queries": 3,
  "api_calls_made": 3,
  "results": {
    "machine learning": { /* same structure as single query */ },
    "deep learning": { /* same structure as single query */ },
    "neural networks": { /* same structure as single query */ }
  },
  "tip": "Batch mode reduces API calls. Use the exact 'name' field when calling other tools."
}
```

#### Match Tiers Explained

Tiers represent the semantic relevance of discovered communities based on vector distance:

| Tier | Distance Range | Meaning | Action |
|------|---|---|---|
| `exact` | 0.0-0.2 | Highly relevant match | Use directly for research |
| `semantic` | 0.2-0.35 | Very relevant, semantically similar | Primary focus communities |
| `adjacent` | 0.35-0.65 | Somewhat relevant, related topics | Secondary communities |
| `peripheral` | 0.65+ | Weakly relevant, tangential connection | Only if other options sparse |

#### Confidence Score Guide

Confidence scores (0.0-1.0) indicate how certain the algorithm is about relevance:

| Confidence Range | Interpretation | Recommended Action |
|---|---|---|
| 0.8-1.0 | Excellent match | Directly relevant, fetch posts immediately |
| 0.7-0.8 | Strong match | Highly relevant, include in batch fetch |
| 0.5-0.7 | Moderate match | Include if coverage is needed |
| 0.4-0.5 | Weak match | Include only if searching for broader perspectives |
| <0.4 | Very weak match | Consider refining search terms |

---

### Helper Tool: `validate_subreddit`

**Purpose:** Verify if a specific subreddit exists in the indexed database.

#### When to Use

- Before calling a subreddit by name in other tools
- When user provides a specific subreddit name
- To check if a community is indexed before fetching

#### Example Responses

**Valid subreddit:**
```json
{
  "valid": true,
  "name": "Python",
  "subscribers": 850000,
  "is_private": false,
  "over_18": false,
  "indexed": true
}
```

**Invalid subreddit:**
```json
{
  "valid": false,
  "name": "xyz_nonexistent",
  "error": "Subreddit 'xyz_nonexistent' not found",
  "suggestion": "Use discover_subreddits to find similar communities"
}
```

---

## 2. Agent Best Practices

### Discovery Workflow

#### Phase 1: Execute Discovery

When initiating research:

```
1. Start with discover_subreddits using topic from user request
2. Always specify limit: 15 (get broader results for evaluation)
3. Only set include_nsfw=true if context requires it
4. Do NOT set min_confidence initially (let server return all)
```

#### Phase 2: Evaluate Results

Analyze the response statistics to decide strategy:

```
Analyze confidence_stats:
- mean > 0.7 → High confidence results (use top 5-8)
- mean 0.5-0.7 → Moderate confidence (use 10-12)
- mean < 0.5 → Low confidence (refine search terms)

Check tier_distribution:
- 5+ "exact" or "semantic" → Proceed to fetch
- Mostly "adjacent" or "peripheral" → Consider alternative search
```

#### Phase 3: Apply Filtering (if needed)

Optionally filter results for precision:

```
If you want only high-quality results:
- Re-query with min_confidence=0.7
- This removes marginal matches
- Reduces token usage in downstream operations

If you want comprehensive coverage:
- Use min_confidence=0.3
- Includes broader topic relationships
```

### Key Decision Points for LLM Agents

#### When to Use `query` vs `queries`

**Use `query` (single topic) when:**
- Searching for one specific topic
- You're unsure about related search terms
- Initial exploration phase

**Use `queries` (batch mode) when:**
- You have 2+ related search terms to explore
- You want comprehensive ecosystem coverage
- Examples: `["machine learning", "deep learning", "neural networks"]`
- **Benefit: 40% fewer API calls than individual queries**

#### When to Set `min_confidence`

**Don't set it (use default 0.0) when:**
- Initial discovery (get full picture)
- You want to see all possibilities
- Coverage matters more than precision
- User request is exploratory

**Set to 0.6+ when:**
- You want only highly relevant communities
- Query was too broad (getting many weak matches)
- Focused research on specific topic
- User asks for expert communities

**Set to 0.7+ when:**
- You need only excellent matches
- Narrow, specific research topic
- You want to minimize noise
- Time/token constraints limit further fetching

#### When to Use `include_nsfw`

- Default `false` for general research
- Only `true` if researching adult-oriented topics explicitly
- Note: NSFW flag filters by category, but results are still ranked by relevance

### Interpreting Response Statistics

#### confidence_stats

Understanding the distribution of match quality:

```json
"confidence_stats": {
  "mean": 0.78,
  "std_dev": 0.08
}
```

**Interpretation:**
- **mean: 0.78** → On average, results are strong (good sign)
- **std_dev: 0.08** → Low variance (consistent quality across results)
- **Action:** All results are similarly relevant; can confidently use many

---

```json
"confidence_stats": {
  "mean": 0.55,
  "std_dev": 0.25
}
```

**Interpretation:**
- **mean: 0.55** → Mixed quality (some good, some weak)
- **std_dev: 0.25** → High variance (inconsistent quality)
- **Action:** Filter by match_tier or apply min_confidence

#### tier_distribution

Understanding coverage across relevance levels:

```json
"tier_distribution": {
  "exact": 8,
  "semantic": 2,
  "adjacent": 0,
  "peripheral": 0
}
```

**Interpretation:** Strong core communities found
- **Action:** Focus on top 8-10 results; high confidence

---

```json
"tier_distribution": {
  "exact": 1,
  "semantic": 2,
  "adjacent": 7,
  "peripheral": 0
}
```

**Interpretation:** Broad matches, not deeply specialized
- **Action:** Either refine search or expand coverage strategy

---

## 3. Usage Examples for Different Scenarios

### Scenario 1: Focused Research on Single Topic

**User Request:** "What do people think about remote work?"

**Agent Action:**
```json
execute_operation("discover_subreddits", {
  "query": "remote work",
  "limit": 15,
  "include_nsfw": false,
  "min_confidence": 0.0
})
```

**Evaluation:**
- If `mean` confidence > 0.7: Proceed with top 8 subreddits
- If `mean` confidence 0.5-0.7: Use 12 subreddits for broader coverage
- If `mean` confidence < 0.5: Try alternative searches like "work from home" or "distributed teams"

**Next Step:** Use `fetch_multiple` with selected subreddit names

---

### Scenario 2: Comprehensive Topic Coverage

**User Request:** "Research Python development best practices"

**Agent Action:**
```json
execute_operation("discover_subreddits", {
  "queries": ["Python", "Django", "FastAPI", "asyncio", "web development"],
  "limit": 10,
  "include_nsfw": false
})
```

**Benefits:**
- Single API call finds all related communities
- Gets 50+ communities vs 10 from single query
- Ensures coverage across entire Python ecosystem
- 40% fewer tokens than individual queries

**Interpretation:**
- Analyze results per topic in batch response
- Identify cross-topic communities (appear in multiple results)
- Select top contributors from each topic area

---

### Scenario 3: High-Precision Research

**User Request:** "Find expert opinions on Kubernetes"

**Agent Action:**
```json
execute_operation("discover_subreddits", {
  "query": "Kubernetes",
  "limit": 20,
  "min_confidence": 0.7
})
```

**Effect:**
- Filters to communities with 0.7+ confidence
- Reduces noise from tangentially-related subreddits
- Ensures expert communities are included
- Results are fewer but higher quality

**Next Step:** Fetch posts from filtered communities with higher confidence in relevance

---

### Scenario 4: Exploratory Research

**User Request:** "What are people discussing about AI safety?"

**Agent Action:**
```json
execute_operation("discover_subreddits", {
  "query": "AI safety",
  "limit": 15,
  "min_confidence": 0.0
})
```

**Evaluation Based on Tier Distribution:**

If mostly "peripheral":
- Retry with more specific terms: "machine learning safety" or "AI ethics"
- Or broaden to "artificial intelligence" and filter results

If many "exact" and "semantic":
- Proceed with batch fetch of top communities
- These are core communities for the topic

---

## 4. Downstream Integration

### Related Tools (Use After Discovery)

Once you have subreddit names from `discover_subreddits`:

| Tool | Parameters | Purpose |
|------|---|---|
| `search_subreddit` | subreddit_name, query, limit | Find specific posts in a community by keyword |
| `fetch_posts` | subreddit_name, listing_type, limit | Get posts from community (hot/new/top/rising) |
| `fetch_multiple` | subreddit_names (array), limit_per_subreddit | **RECOMMENDED:** Batch fetch from multiple communities |
| `fetch_comments` | submission_id or url, comment_limit | Get complete comment trees for deep analysis |

### Typical Research Flow

```
STEP 1: discover_subreddits()
   ↓
[Get subreddit names with confidence scores]
   ↓
STEP 2: fetch_multiple() [Use names from discovery]
   ↓
[Get posts from multiple communities]
   ↓
STEP 3: fetch_comments() [On high-engagement posts]
   ↓
[Analyze comments from 50-100 comments across 5-10 posts]
   ↓
STEP 4: Synthesize findings into research report
```

### Using Discovery Results

When calling downstream tools, use the exact `name` field from discovery results:

```json
// From discover_subreddits result:
{
  "name": "MachineLearning",  // ← Use this exact value
  "confidence": 0.89,
  ...
}

// Pass to fetch_multiple:
execute_operation("fetch_multiple", {
  "subreddit_names": ["MachineLearning", "learnmachinelearning", "DeepLearning"],
  "limit_per_subreddit": 10
})
```

---

## 5. Error Handling & Recovery

### Common Errors and Recovery Strategies

| Error | Cause | Recovery |
|-------|-------|----------|
| No results returned | Too specific or unusual query | Try broader term: "machine learning" → "AI" |
| All results < 0.4 confidence | Query doesn't match 20K indexed communities | Try alternative phrasing or acronyms |
| NSFW communities appearing | include_nsfw=true when not intended | Re-query with include_nsfw=false |
| Subreddit "not found" | Typo, name change, or private subreddit | Use discover to find correct current name |
| High std_dev in stats | Inconsistent relevance across results | Filter with min_confidence or use match_tier |

### Recovery Strategies by Situation

**If confidence_stats.mean < 0.5:**
```
Option 1: Refine search terms
- Try synonyms: "machine learning" → "AI" or "neural networks"
- Be more specific: "python" → "python web development"

Option 2: Expand search scope
- Use queries (batch mode) with related terms
- Example: ["AI", "machine learning", "deep learning", "neural networks"]

Option 3: Lower confidence threshold
- Accept lower confidence results with min_confidence=0.3
- Increases coverage but may introduce noise
```

**If tier_distribution shows mostly "adjacent" or "peripheral":**
```
Action 1: Try alternative phrasing
- Original: "remote work" → Alternative: "work from home"
- Original: "async programming" → Alternative: "asynchronous python"

Action 2: Check if topic is in 20K indexed communities
- Use validate_subreddit for known related communities
- May indicate your topic is too niche

Action 3: Use broader parent topic
- Specific: "Kubernetes" → Broader: "DevOps"
- Specific: "FastAPI" → Broader: "Python web frameworks"
```

---

## 6. Token Optimization for LLM Agents

### Estimated Token Usage

- **discover_subreddits** (single query): 500-800 tokens
- **discover_subreddits** (batch 5 queries): 1,500-2,000 tokens
  - Individual queries would cost: 2,500-4,000 tokens
  - Batch savings: ~40% reduction
- **fetch_multiple** (10 subreddits): 3,000-5,000 tokens
- **fetch_comments** (100 comments): 2,000-4,000 tokens
- **Complete research workflow** (discovery → fetch → analyze): 15-20K tokens

### Optimization Strategies

**Strategy 1: Use Batch Mode for Multiple Topics**
```
❌ INEFFICIENT:
- Call discover_subreddits 5 times (one per topic)
- Cost: ~2,500-4,000 tokens

✅ EFFICIENT:
- Call discover_subreddits once with queries parameter
- Cost: ~1,500-2,000 tokens
- Saves: ~40%
```

**Strategy 2: Apply Confidence Filtering Early**
```
❌ INEFFICIENT:
- Get all results (50+ from batch)
- Fetch all 50 communities
- Filter by confidence during analysis
- Cost: Heavy in downstream tools

✅ EFFICIENT:
- Set min_confidence=0.6 in discover
- Get only ~20 high-quality results
- Fetch only relevant communities
- Cost: ~30% reduction overall
```

**Strategy 3: Set Appropriate Limits**
```
❌ INEFFICIENT:
- Set limit: 50 (get everything)
- Fetch all 50 subreddits
- Most aren't used

✅ EFFICIENT:
- Set limit: 10-15 (evaluation set)
- Evaluate confidence_stats
- Fetch only 5-10 top results
- Cost: Proportional to actual needs
```

### Typical Token Budget

For comprehensive research within reasonable limits:

```
Phase 1 - Discovery: ~1,500 tokens
Phase 2 - Fetch posts (10 subreddits): ~4,000 tokens
Phase 3 - Fetch comments (10 posts): ~3,000 tokens
Phase 4 - Analysis and synthesis: ~5,000 tokens

Total: ~13,500 tokens for thorough research
```

---

## 7. Advanced Configuration (For Server Administrators)

### SearchConfig Parameters

Server administrators can customize search behavior by deploying with different SearchConfig defaults:

| Parameter | Default | Typical Range | Effect |
|-----------|---------|---|---|
| `EXACT_DISTANCE_THRESHOLD` | 0.2 | 0.15-0.3 | Stricter = fewer "exact" matches |
| `SEMANTIC_DISTANCE_THRESHOLD` | 0.35 | 0.3-0.5 | Affects "semantic" tier classification |
| `GENERIC_PENALTY_MULTIPLIER` | 0.3 | 0.1-0.5 | Lower = harsher on generic communities |
| `LARGE_SUB_BOOST_MULTIPLIER` | 1.1 | 1.0-1.2 | Higher = favor larger communities |
| `CONFIDENCE_DISTANCE_BREAKPOINTS` | (see code) | Customizable | Custom distance-to-confidence mapping |

---

## 8. Quick Reference

### Parameter Cheat Sheet

| Goal | Parameters |
|------|---|
| Broad exploration | `query`, `limit: 15`, `min_confidence: 0.0` |
| Multiple topics | `queries: ["term1", "term2"]`, `limit: 10` |
| High precision | `query`, `min_confidence: 0.7`, `limit: 20` |
| Comprehensive coverage | `queries` with 5+ terms, `limit: 10` |
| NSFW research | `query`, `include_nsfw: true` |

### Interpretation Cheat Sheet

| Statistic | What It Means | Action |
|---|---|---|
| `mean > 0.7` | Strong matches overall | Proceed with discovery results |
| `std_dev < 0.1` | Consistent quality | All results equally useful |
| `tier_distribution: exact: 5+` | Core communities found | Focus on top communities |
| `has_more: true` | 50+ results exist | Consider min_confidence filter |

---

## 9. Examples in Context

### Example 1: Tech Decision Research

**User:** "How do developers feel about Rust vs Go?"

**Agent Approach:**
```json
// Batch discover related communities
execute_operation("discover_subreddits", {
  "queries": ["Rust programming", "Go language", "systems programming", "performance"],
  "limit": 10
})

// Results show mean confidence: 0.82, mostly "exact"/"semantic"
// Decision: Proceed with all 40 communities found

execute_operation("fetch_multiple", {
  "subreddit_names": [...extracted from discovery...],
  "listing_type": "top",
  "time_filter": "year",
  "limit_per_subreddit": 10
})

// Fetch 100 posts, analyze sentiment and discussion
```

### Example 2: Market Research

**User:** "What's the current sentiment on electric vehicles?"

**Agent Approach:**
```json
execute_operation("discover_subreddits", {
  "queries": ["electric vehicles", "Tesla", "EV", "sustainable transport"],
  "limit": 15
})

// Analyze confidence_stats: mean 0.71
// Tier distribution shows good coverage

// Set min_confidence=0.6 for second pass if needed
execute_operation("discover_subreddits", {
  "queries": ["electric vehicles", "Tesla", "EV", "sustainable transport"],
  "limit": 15,
  "min_confidence": 0.6
})

// Get 30 high-confidence communities
// Fetch from top 10-12 by confidence
```

---

## 10. Troubleshooting Guide

### Problem: "Got too many tangential results"

**Diagnosis:** Likely tier_distribution has many "adjacent"/"peripheral" entries

**Solutions:**
1. Re-query with `min_confidence: 0.6`
2. Use more specific search terms
3. Try batch mode with related specific terms instead of broad term

### Problem: "Not enough results for comprehensive analysis"

**Diagnosis:** Low confidence_stats.mean (<0.5)

**Solutions:**
1. Try alternative search terms
2. Use batch mode with 5+ related terms
3. Lower min_confidence to 0.3 (accept broader matches)

### Problem: "Can't find specific community I need"

**Solution:**
1. Use `validate_subreddit` with the specific name
2. If not found, use `discover_subreddits` to find related communities
3. May indicate subreddit is private or not indexed

---

## 11. Summary Table: When to Use What

| Research Type | Tool | Key Parameters | Result Count | Quality |
|---|---|---|---|---|
| Single specific topic | `discover_subreddits` with `query` | `limit: 15`, `min_confidence: 0.0` | 10-50 | Mixed |
| Multiple related topics | `discover_subreddits` with `queries` | 5 terms, `limit: 10` | 30-80 | Good |
| Expert communities only | `discover_subreddits` with `query` | `min_confidence: 0.7`, `limit: 20` | 5-15 | Excellent |
| Broad coverage | `discover_subreddits` with `queries` | Many terms, `limit: 10` | 50-150 | Varies |

---

**Document Version:** 1.0
**Last Updated:** 2024-11-05
**MCP Server Version:** Compatible with 0.4.0+