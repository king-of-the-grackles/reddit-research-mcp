# Reddit MCP Server

MCP server for Reddit access with semantic search and batch operations. Built with FastMCP for efficient LLM integration.

## Features

- **Semantic Discovery**: Find 8-15 relevant subreddits using vector search
- **Batch Operations**: Fetch from multiple subreddits in one call (70% fewer API calls)
- **Three-Layer Architecture**: Discovery → Requirements → Execution workflow
- **Full Citations**: Reddit URLs included in all results
- **Deep Analysis**: Complete comment trees for thorough research

## How It Works

### Subreddit Discovery with Vector Search
Reddit's native subreddit discovery API is limited and often returns irrelevant results. To solve this, we've indexed all active subreddits with 5,000+ subscribers into a vector database using ChromaDB. This enables semantic search that understands context and relationships between topics, finding relevant communities that keyword search would miss.

### Batch Operations
Instead of making sequential API calls to fetch from multiple subreddits, `fetch_multiple` retrieves posts from up to 15 subreddits in a single operation. This reduces API calls by 70% and significantly improves response times for comprehensive research tasks.

### Three-Layer Architecture
The server guides LLMs through a structured workflow: Discovery finds relevant resources, Requirements provides parameter schemas and validation, and Execution performs the actual Reddit operations. This design prevents errors and ensures LLMs use the API efficiently.

## Claude Code Research Agent

This project includes a specialized Claude Code agent for automated Reddit research. The agent conducts comprehensive community analysis across multiple subreddits and produces detailed markdown reports with full citations.

**What it does:**
- Automatically discovers and analyzes 10+ relevant subreddits
- Gathers 100+ comments from high-engagement discussions
- Synthesizes findings into Obsidian-compatible markdown reports
- Includes clickable Reddit URLs for every citation
- Tracks sentiment, temporal trends, and community consensus

**Usage in Claude Code:**
```bash
# After MCP server is connected, simply ask:
"Research [topic] on Reddit using the research agent"
```

The agent handles the entire workflow automatically and saves the report to `/reports/[topic]-YYYY-MM-DD.md`. See [agent configuration](src/.claude/agents/reddit-research-agent.md) for full capabilities.

## What Makes This Server Unique?

This server is specifically designed for **comprehensive Reddit research** rather than just browsing. Here's what sets it apart:

### 🔍 Semantic Subreddit Discovery
Most Reddit tools require you to know which subreddits to search. This server has **indexed 20,000+ active subreddits** into a vector database, enabling semantic search that finds relevant communities you didn't know existed. Ask about any topic and discover 8-15 related subreddits automatically.

### ⚡ Efficient Batch Operations
The `fetch_multiple` operation retrieves posts from up to 15 subreddits in a single call, reducing API calls by 70% compared to sequential fetching. This means faster results and fewer rate limit issues.

### 🎯 Research-Optimized Workflow
The three-layer architecture (Discovery → Requirements → Execution) guides LLMs through complex research tasks, preventing common errors and ensuring comprehensive coverage across multiple communities.

### 📊 Automated Analysis & Reporting
Includes a Claude Code agent that automatically conducts research across 10+ subreddits, analyzes 100+ comments, and produces professional markdown reports with full citations - turning hours of manual work into a single command.

## Quick Start

### Prerequisites
- Python 3.11+
- Reddit API credentials ([Get them here](https://www.reddit.com/prefs/apps))

### Setup

1. Clone and install:
```bash
git clone https://github.com/king-of-the-grackles/reddit-research-mcp.git
cd reddit-research-mcp
pip install uv
uv sync
```

2. Configure `.env`:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=RedditMCP/1.0
```

3. Run server:
```bash
uv run src/server.py
```

### Claude Code Integration

Add to Claude Code:
```bash
claude mcp add -s user -t stdio reddit-mcp-poc uv run fastmcp run <FULL_PATH>/src/server.py
```

Verify connection:
```bash
claude mcp list
```

## Usage

### Three-Layer Workflow

```python
# 1. DISCOVERY - Find communities
discover_operations()

# 2. REQUIREMENTS - Get parameters (optional)
get_operation_schema("fetch_multiple")

# 3. EXECUTION - Fetch content
execute_operation("fetch_multiple", {
    "subreddit_names": ["MachineLearning", "artificial"],
    "limit_per_subreddit": 8
})
```

### Quick Operations

```python
# Search across Reddit
execute_operation("search_all", {
    "query": "AI ethics",
    "limit": 15
})

# Get comments for analysis
execute_operation("fetch_comments", {
    "submission_id": "abc123",
    "comment_limit": 100
})
```

## Available Operations

**Core Operations:**
- `discover_subreddits` - Semantic search for communities
- `search_all` - Search across Reddit
- `search_subreddit` - Search within a community
- `fetch_posts` - Get posts from one subreddit
- `fetch_multiple` - Batch fetch from multiple subreddits
- `fetch_comments` - Get full comment trees

**MCP Resources:**
- `reddit://popular-subreddits` - Top 25 subreddits
- `reddit://subreddit/{name}/about` - Subreddit details
- `reddit://server-info` - Server capabilities

## Project Structure

```
reddit-mcp-poc/
├── src/
│   ├── server.py           # Main MCP server
│   ├── config.py           # Reddit client setup
│   ├── resources.py        # MCP resources
│   └── tools/              
│       ├── search.py       # Search operations
│       ├── posts.py        # Post fetching
│       ├── comments.py     # Comment retrieval
│       ├── discover.py     # Subreddit discovery
│       └── db/             # Vector search database
├── tests/
├── pyproject.toml
└── .env
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Reddit API credentials not found" | Check `.env` file exists with valid credentials |
| Rate limit errors | Wait a few minutes; handled automatically |
| "Subreddit not found" | Verify subreddit name (without r/ prefix) |

## License

MIT