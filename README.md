# 🔍 Reddit Research MCP Server

**Turn Reddit's chaos into structured insights with full citations**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/Built%20with-FastMCP-orange.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
codex -c 'mcp_servers.reddit-research-mcp.command=npx' \
      -c 'mcp_servers.reddit-research-mcp.args=["-y", "mcp-remote@latest", "https://reddit-research-mcp.fastmcp.app/mcp"]'
```

### Gemini CLI
```bash
gemini mcp add reddit-research-mcp https://reddit-research-mcp.fastmcp.app/mcp --transport http
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

---

## ✨ Why This Server?

**Built for decision-makers who need evidence-based insights.** Every report links back to actual Reddit posts and comments. When you say "users are complaining about X," you'll have the receipts to prove it. Check the `/reports` folder for examples of deep-research reports with full citation trails.

**Zero-friction setup designed for non-technical users.** Most MCP servers require cloning repos, managing Python environments, and hunting for API keys in developer dashboards. This one? Just paste the URL into Claude and start researching. Our hosted solution means no terminal commands, no credential management, no setup headaches.

**Semantic search across 20,000+ active subreddits.** Reddit's API caps at 250 search results - useless for comprehensive research. We pre-indexed every active subreddit (2k+ members, active in last 7 days) with vector embeddings. Now you search conceptually across all of Reddit, finding relevant communities you didn't even know existed. Built with the [layered abstraction pattern](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers) for scalability.

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
<summary><strong>🛠️ Core MCP Tools</strong></summary>

#### Discover Communities
```python
execute_operation("discover_subreddits", {
    "topic": "machine learning",
    "limit": 15
})
```

#### Search Across Reddit
```python
execute_operation("search_all", {
    "query": "ChatGPT experiences",
    "time_filter": "week",
    "limit": 25
})
```

#### Batch Fetch Posts
```python
execute_operation("fetch_multiple", {
    "subreddit_names": ["technology", "programming"],
    "limit_per_subreddit": 10,
    "time_filter": "day"
})
```

#### Deep Dive with Comments
```python
execute_operation("fetch_comments", {
    "submission_id": "abc123",
    "comment_limit": 200,
    "sort": "best"
})
```
</details>

<details>
<summary><strong>📁 Project Structure</strong></summary>

```
reddit-research-mcp/
├── src/
│   ├── server.py          # FastMCP server
│   ├── config.py          # Reddit configuration
│   ├── chroma_client.py   # Vector database proxy
│   ├── resources.py       # MCP resources
│   ├── models.py          # Data models
│   └── tools/
│       ├── search.py      # Search operations
│       ├── posts.py       # Post fetching
│       ├── comments.py    # Comment retrieval
│       └── discover.py    # Subreddit discovery
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

---

<div align="center">

**Stop guessing. Start knowing what your market actually thinks.**

[GitHub](https://github.com/king-of-the-grackles/reddit-research-mcp) • [Report Issues](https://github.com/king-of-the-grackles/reddit-research-mcp/issues) • [Request Features](https://github.com/king-of-the-grackles/reddit-research-mcp/issues)

</div>