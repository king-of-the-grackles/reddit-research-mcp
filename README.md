mcp-name: io.github.king-of-the-grackles/reddit-research-mcp

# 🔍 Reddit Research MCP Server

**Turn Reddit's chaos into structured insights with full citations**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/Built%20with-FastMCP-orange.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Version**: 0.4.0

**What's New in 0.4.0:**
- ✨ Added 5 feed management operations for persistent research
- 🏗️ Enhanced three-layer architecture with comprehensive schemas
- 🤖 Added reddit_research prompt for automated workflows
- 🔧 Improved error handling and recovery suggestions
- 📝 Complete terminology migration (watchlist → feed)

---

Your customers are on Reddit right now, comparing you to competitors, sharing pain points, requesting features. But finding those insights means hours of manual searching with no way to cite your sources.

This MCP server turns Reddit into a queryable research database that generates reports with links to every claim. Get comprehensive market research, competitive analysis, and customer insights in minutes instead of hours.

---

## 🚀 Quick Setup (60 Seconds)

**No credentials or configuration needed!** Connect to our hosted server:

### Claude Code
```bash
claude mcp add --scope local --transport http reddit-research-mcp https://reddit-research-mcp.fastmcp.app/mcp
```

### Cursor
```
cursor://anysphere.cursor-deeplink/mcp/install?name=reddit-research-mcp&config=eyJ1cmwiOiJodHRwczovL3JlZGRpdC1yZXNlYXJjaC1tY3AuZmFzdG1jcC5hcHAvbWNwIn0%3D
```

### OpenAI Codex CLI
```bash
codex mcp add reddit-research-mcp \
    npx -y mcp-remote \
    https://reddit-research-mcp.fastmcp.app/mcp \
    --auth-timeout 120 \
    --allow-http \
```

### Gemini CLI
```bash
gemini mcp add reddit-research-mcp \
  npx -y mcp-remote \
  https://reddit-research-mcp.fastmcp.app/mcp \
  --auth-timeout 120 \
  --allow-http
```

### Direct MCP Server URL
For other AI assistants: `https://reddit-research-mcp.fastmcp.app/mcp`

---

## 🎯 What You Can Do

### Competitive Analysis
```
"What are developers saying about Next.js vs Remix?"
```
→ Get a comprehensive report comparing sentiment, feature requests, pain points, and migration experiences with links to every mentioned discussion.

### Customer Discovery
```
"Find the top complaints about existing CRM tools in small business communities"
```
→ Discover unmet needs, feature gaps, and pricing concerns directly from your target market with citations to real user feedback.

### Market Research
```
"Analyze sentiment about AI coding assistants across developer communities"
```
→ Track adoption trends, concerns, success stories, and emerging use cases with temporal analysis showing how opinions evolved.

### Product Validation
```
"What problems are SaaS founders having with subscription billing?"
```
→ Identify pain points and validate your solution with evidence from actual discussions, not assumptions.

### Long-Term Monitoring
```
"Track evolving sentiment about your product category across 10+ communities"
```
→ Create a feed with relevant subreddits and periodically check for new insights without starting research from scratch each time.

---

## ✨ Why This Server?

**Built for decision-makers who need evidence-based insights.** Every report links back to actual Reddit posts and comments. When you say "users are complaining about X," you'll have the receipts to prove it. Check the `/reports` folder for examples of deep-research reports with full citation trails.

**Zero-friction setup designed for non-technical users.** Most MCP servers require cloning repos, managing Python environments, and hunting for API keys in developer dashboards. This one? Just paste the URL into Claude and start researching. Our hosted solution means no terminal commands, no credential management, no setup headaches.

**Semantic search across 20,000+ active subreddits.** Reddit's API caps at 250 search results - useless for comprehensive research. We pre-indexed every active subreddit (2k+ members, active in last 7 days) with vector embeddings. Now you search conceptually across all of Reddit, finding relevant communities you didn't even know existed. Built with the [layered abstraction pattern](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers) for scalability.

**Persistent research management.** Save your subreddit lists, analyses, and configurations into feeds for ongoing monitoring. Track what matters without starting from scratch each time. Perfect for long-term competitive analysis, market research campaigns, and product validation projects.

---

## 📊 Server Statistics

- **MCP Tools**: 3 (discover_operations, get_operation_schema, execute_operation)
- **Reddit Operations**: 5 (discover, search, fetch_posts, fetch_multiple, fetch_comments)
- **Feed Operations**: 5 (create, list, get, update, delete)
- **Indexed Subreddits**: 20,000+ (2k+ members, active in last 7 days)
- **MCP Prompts**: 1 (reddit_research for automated workflows)
- **Resources**: 1 (reddit://server-info for comprehensive documentation)

---

## 📚 Specifications

Some of the AI-generated specs that were used to build this project with Claude Code:
- 📖 [Architecture Overview](specs/agentic-discovery-architecture.md) - System design and component interaction
- 🤖 [Research Agent Details](specs/reddit-research-agent-spec.md) - Agent implementation patterns
- 🔍 [Deep Research Architecture](specs/deep-research-reddit-architecture.md) - Research workflow and citation system
- 🗄️ [ChromaDB Proxy Architecture](specs/chroma-proxy-architecture.md) - Vector search and authentication layer

---

## Technical Details

<details>
<summary><strong>🏗️ Three-Layer MCP Architecture</strong></summary>

This server follows the **layered abstraction pattern** for scalability and self-documentation:

### Layer 1: Discovery
```python
discover_operations()
```
**Purpose**: See what operations are available and get workflow recommendations.

**Returns**: List of all operations (Reddit research + feed management) with descriptions and recommended workflows.

### Layer 2: Schema Inspection
```python
get_operation_schema("discover_subreddits", include_examples=True)
```
**Purpose**: Understand parameter requirements, validation rules, and see examples before executing.

**Returns**: Complete schema with parameter types, descriptions, ranges, and usage examples.

### Layer 3: Execution
```python
execute_operation("discover_subreddits", {
    "query": "machine learning",
    "limit": 15,
    "min_confidence": 0.6
})
```
**Purpose**: Perform the actual operation with validated parameters.

**Returns**: Operation results wrapped in `{"success": bool, "data": ...}` format.

---

### Why This Pattern?

- **Self-documenting**: Operations describe their own requirements
- **Version-safe**: Schema changes don't break existing clients
- **Extensible**: Add new operations without changing core tools
- **Type-safe**: Full validation before execution

### Example Workflow

```python
# Step 1: Discover available operations
result = discover_operations()
# Shows: discover_subreddits, search_subreddit, fetch_posts, fetch_multiple,
#        fetch_comments, create_feed, list_feeds, get_feed, update_feed, delete_feed

# Step 2: Get schema for the operation you want to use
schema = get_operation_schema("discover_subreddits", include_examples=True)
# Returns parameter types, validation rules, and examples

# Step 3: Execute with validated parameters
communities = execute_operation("discover_subreddits", {
    "query": "artificial intelligence ethics",
    "limit": 20,
    "min_confidence": 0.7,
    "include_nsfw": False
})
```

</details>

<details>
<summary><strong>🔧 Reddit Research Operations (5)</strong></summary>

### discover_subreddits
Find relevant communities using semantic vector search across 20,000+ indexed subreddits.

```python
execute_operation("discover_subreddits", {
    "query": "machine learning frameworks",
    "limit": 15,
    "min_confidence": 0.6,
    "include_nsfw": False
})
```

**Returns**: Communities with confidence scores (0-1), match tiers, subscribers, and descriptions.

**Use for**: Starting any research project, finding niche communities, validating topic coverage.

---

### search_subreddit
Search for posts within a specific subreddit.

```python
execute_operation("search_subreddit", {
    "subreddit_name": "MachineLearning",
    "query": "transformer architectures",
    "sort": "relevance",
    "time_filter": "month",
    "limit": 25
})
```

**Returns**: Posts matching the search query with scores, comments, and timestamps.

**Use for**: Deep-diving into specific communities, finding historical discussions.

---

### fetch_posts
Get posts from a single subreddit by listing type (hot, new, top, rising).

```python
execute_operation("fetch_posts", {
    "subreddit_name": "technology",
    "listing_type": "top",
    "time_filter": "week",
    "limit": 20
})
```

**Returns**: Recent posts from the subreddit with scores, comments, and authors.

**Use for**: Monitoring specific communities, trend analysis, content curation.

---

### fetch_multiple
**70% more efficient** - Batch fetch posts from multiple subreddits concurrently.

```python
execute_operation("fetch_multiple", {
    "subreddit_names": ["Python", "django", "flask"],
    "listing_type": "hot",
    "limit_per_subreddit": 10,
    "time_filter": "day"
})
```

**Returns**: Posts from all specified subreddits, organized by community.

**Use for**: Comparative analysis, multi-community research, feed monitoring.

---

### fetch_comments
Get complete comment tree for deep analysis of discussions.

```python
execute_operation("fetch_comments", {
    "submission_id": "abc123",
    "comment_limit": 100,
    "comment_sort": "best"
})
```

**Returns**: Post details + nested comment tree with scores, authors, and timestamps.

**Use for**: Understanding community sentiment, identifying expert opinions, analyzing debates.

</details>

<details>
<summary><strong>📊 Feed Management Operations (5)</strong></summary>

**Feeds let you save research configurations for ongoing monitoring.** Perfect for long-term projects, competitive analysis, and market research campaigns.

### create_feed
Save discovered subreddits with analysis and metadata.

```python
execute_operation("create_feed", {
    "name": "AI Research Communities",
    "website_url": "https://example.com",
    "analysis": {
        "description": "AI/ML communities for technical discussions",
        "audience_personas": ["ML engineers", "researchers", "data scientists"],
        "keywords": ["machine learning", "deep learning", "neural networks"]
    },
    "selected_subreddits": [
        {
            "name": "MachineLearning",
            "description": "ML community",
            "subscribers": 2500000,
            "confidence_score": 0.85
        },
        {
            "name": "deeplearning",
            "description": "Deep learning discussions",
            "subscribers": 150000,
            "confidence_score": 0.92
        }
    ]
})
```

**Returns**: Created feed with UUID, timestamps, and metadata.

**Use for**: Starting long-term research projects, saving competitive analysis configurations.

---

### list_feeds
View all your saved feeds with pagination.

```python
execute_operation("list_feeds", {
    "limit": 10,
    "offset": 0
})
```

**Returns**: Array of feeds with metadata, sorted by recently viewed.

**Use for**: Managing multiple research projects, reviewing saved configurations.

---

### get_feed
Retrieve a specific feed by ID.

```python
execute_operation("get_feed", {
    "feed_id": "550e8400-e29b-41d4-a716-446655440000"
})
```

**Returns**: Complete feed details including subreddits, analysis, and metadata.

**Use for**: Resuming research projects, reviewing feed configurations.

---

### update_feed
Modify feed name, subreddits, or analysis (partial updates supported).

```python
execute_operation("update_feed", {
    "feed_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Updated Feed Name",
    "selected_subreddits": [
        # Add or replace subreddits
    ]
})
```

**Returns**: Updated feed with new timestamps.

**Use for**: Refining research scope, adding newly discovered communities.

---

### delete_feed
Remove a feed permanently.

```python
execute_operation("delete_feed", {
    "feed_id": "550e8400-e29b-41d4-a716-446655440000"
})
```

**Returns**: Confirmation of deletion.

**Use for**: Cleaning up completed projects, removing outdated configurations.

---

### Feed Workflow Example

```python
# 1. Discover relevant subreddits
communities = execute_operation("discover_subreddits", {
    "query": "sustainable energy technology",
    "limit": 20
})

# 2. Create a feed with selected communities
feed = execute_operation("create_feed", {
    "name": "Clean Energy Research",
    "analysis": {
        "description": "Communities discussing renewable energy and sustainability",
        "audience_personas": ["engineers", "researchers", "policy makers"],
        "keywords": ["solar", "wind", "battery", "sustainable"]
    },
    "selected_subreddits": communities["data"]["subreddits"][:10]
})

# 3. Later: Resume research from saved feed
saved_feed = execute_operation("get_feed", {
    "feed_id": feed["data"]["id"]
})

# 4. Fetch posts from feed subreddits
posts = execute_operation("fetch_multiple", {
    "subreddit_names": [sub["name"] for sub in saved_feed["data"]["selected_subreddits"]],
    "listing_type": "hot",
    "limit_per_subreddit": 5
})
```

</details>

<details>
<summary><strong>🔐 Authentication</strong></summary>

This server uses **Descope OAuth2** for secure authentication:

- **Type**: OAuth2 with Descope provider
- **Scope**: Read-only access to public Reddit content
- **Setup**: No Reddit credentials needed - server handles authentication
- **Token**: Automatically managed by your MCP client
- **Privacy**: Only accesses public Reddit data, no personal information collected

Your AI assistant will prompt for authentication on first use. The process takes ~30 seconds and only needs to be done once.

</details>

<details>
<summary><strong>🔧 Error Handling</strong></summary>

The server provides intelligent recovery suggestions for common errors:

### 404 Not Found
**Cause**: Subreddit doesn't exist or name is misspelled
**Recovery**: Verify the subreddit name or use `discover_subreddits` to find communities

### 429 Rate Limited
**Cause**: Too many requests to Reddit API (60 requests/minute limit)
**Recovery**: Reduce the `limit` parameter or wait 30 seconds before retrying

### 403 Private/Forbidden
**Cause**: Subreddit is private, quarantined, or banned
**Recovery**: Try other communities from your discovery results

### 422 Validation Error
**Cause**: Parameters don't match schema requirements
**Recovery**: Use `get_operation_schema()` to check parameter types and validation rules

### 401 Authentication Required
**Cause**: Descope token expired or invalid
**Recovery**: Re-authenticate when prompted by your AI assistant

</details>

<details>
<summary><strong>📁 Project Structure</strong></summary>

```
reddit-research-mcp/
├── src/
│   ├── server.py          # FastMCP server with 3-layer architecture
│   ├── config.py          # Reddit API configuration
│   ├── chroma_client.py   # Vector database proxy
│   ├── resources.py       # MCP resources
│   ├── models.py          # Data models
│   └── tools/
│       ├── search.py      # Search operations
│       ├── posts.py       # Post fetching
│       ├── comments.py    # Comment retrieval
│       ├── discover.py    # Subreddit discovery
│       └── feed.py        # Feed CRUD operations
├── tests/                 # Test suite
├── reports/               # Example reports
└── specs/                 # Architecture docs
```
</details>

<details>
<summary><strong>🚀 Contributing & Tech Stack</strong></summary>

This project uses:
- Python 3.11+ with type hints
- FastMCP for the server framework
- Vector search via authenticated proxy (Render.com)
- ChromaDB for semantic search
- PRAW for Reddit API interaction
- httpx for HTTP client requests (feed operations)

</details>

---

<div align="center">

**Stop guessing. Start knowing what your market actually thinks.**

[GitHub](https://github.com/king-of-the-grackles/reddit-research-mcp) • [Report Issues](https://github.com/king-of-the-grackles/reddit-research-mcp/issues) • [Request Features](https://github.com/king-of-the-grackles/reddit-research-mcp/issues)

</div>
