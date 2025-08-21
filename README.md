# 🔍 Reddit Research MCP Server

> **Transform Reddit into your personal research assistant** - Semantic search across 20,000+ communities with AI-powered analysis

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/Built%20with-FastMCP-orange.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Why This Server?

**Stop manually searching through Reddit.** This MCP server transforms Reddit into a structured research tool that:

- 🎯 **Discovers relevant communities you didn't know existed** - Semantic search across 20,000+ indexed subreddits
- ⚡ **Reduces API calls by 70%** - Batch operations fetch from 15 subreddits simultaneously  
- 🤖 **Automates comprehensive research** - Built-in Claude Code agent analyzes 100+ posts and comments
- 📊 **Produces professional reports** - Markdown output with full citations and sentiment analysis
- 🔗 **Provides complete traceability** - Every insight linked to its Reddit source

---

## 🚀 Quick Start (60 Seconds)

### Prerequisites
- 🐍 Python 3.11+
- 🔑 Reddit API credentials ([Get them here](https://www.reddit.com/prefs/apps) - takes 2 minutes)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/king-of-the-grackles/reddit-research-mcp.git
cd reddit-research-mcp

# 2. Install dependencies
pip install uv
uv sync

# 3. Add your Reddit credentials
cp .env.sample .env
# Edit .env with your credentials

# 4. Run the server
uv run src/server.py
```

---

## 🔑 Getting Your Reddit API Credentials

Before using the server, you'll need Reddit API credentials. This takes about 2 minutes:

1. **Go to Reddit App Preferences**
   - Visit [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) while logged into Reddit
   
2. **Create a New App**
   - Click "Create App" or "Create Another App"
   - Fill in the form:
     - **Name**: `MCP Research Tool` (or any name you prefer)
     - **App Type**: Select `script` (for personal use)
     - **Description**: Optional - can leave blank
     - **About URL**: Optional - can leave blank
     - **Redirect URI**: `http://localhost:8080` (required but not used)
   - Click "Create app"

3. **Get Your Credentials**
   - **Client ID**: The string under "personal use script" (looks like: `abc123def456`)
   - **Client Secret**: The string next to "secret" (looks like: `ghi789jkl012mno345pqr678`)
   - **User Agent**: Create one like: `MCP:research:v1.0 (by /u/yourusername)`

### Security Notes

- ✅ The server only requests read-only access to public Reddit data
- 🚫 No Reddit account login required - the app uses app-only authentication

---

## 🎨 Key Features

### 🔍 **Semantic Subreddit Discovery**
Unlike Reddit's limited native search, our vector database indexes 20,000+ active communities, understanding context and relationships to find relevant subreddits you never knew existed.

```python
# Discover communities about "sustainable living"
# Returns: ZeroWaste, BuyItForLife, Permaculture, SimpleLiving, and 10+ more
```

### ⚡ **Intelligent Batch Operations**
Fetch posts from up to 15 subreddits in a single API call - 70% more efficient than sequential requests.

```python
# One call instead of fifteen
execute_operation("fetch_multiple", {
    "subreddit_names": ["MachineLearning", "artificial", "deeplearning", ...],
    "limit_per_subreddit": 10
})
```

### 🤖 **Automated Research Agent**
A specialized Claude Code agent that conducts end-to-end research:

```bash
# In Claude Code, simply say:
"Research cryptocurrency regulation on Reddit"

# The agent automatically:
# → Discovers 15+ relevant crypto communities
# → Analyzes 100+ posts and comments
# → Generates a comprehensive report with citations
# → Saves to /reports/cryptocurrency-regulation-2025-01-19.md
```

### 🏗️ **Three-Layer Architecture**
Guides LLMs through complex operations with built-in error prevention:

1. **Discovery** → Find relevant resources
2. **Requirements** → Validate parameters
3. **Execution** → Perform operations safely

---

## 📖 How to Use

### 🔌 Claude Code Integration

```bash
# Add the server to Claude Code
claude mcp add -s user -t stdio reddit-research-mcp \
  uv run fastmcp run /path/to/reddit-research-mcp/src/server.py

# Verify connection
claude mcp list
```

### 🛠️ Core Operations

#### Discover Communities
```python
# Find subreddits about any topic
execute_operation("discover_subreddits", {
    "topic": "machine learning",
    "limit": 15
})
```

#### Search Across Reddit
```python
# Search all of Reddit
execute_operation("search_all", {
    "query": "ChatGPT experiences",
    "time_filter": "week",
    "limit": 25
})
```

#### Batch Fetch Posts
```python
# Get posts from multiple subreddits at once
execute_operation("fetch_multiple", {
    "subreddit_names": ["technology", "programming", "coding"],
    "limit_per_subreddit": 10,
    "time_filter": "day"
})
```

#### Deep Dive with Comments
```python
# Analyze full discussions
execute_operation("fetch_comments", {
    "submission_id": "abc123",
    "comment_limit": 200,
    "sort": "best"
})
```

---

## 🗂️ Project Structure

```
reddit-research-mcp/
├── 📁 src/
│   ├── 🚀 server.py          # FastMCP server
│   ├── 🔧 config.py          # Reddit client configuration
│   ├── 📚 resources.py       # MCP resources
│   └── 🛠️ tools/
│       ├── 🔍 search.py      # Search operations
│       ├── 📝 posts.py       # Post fetching
│       ├── 💬 comments.py    # Comment retrieval
│       ├── 🎯 discover.py    # Subreddit discovery
│       └── 🗄️ db/           # Vector database (20k+ subreddits)
├── 📊 reports/               # Generated research reports
├── 📋 specs/                 # Architecture documentation
└── 🔐 .env                  # Your credentials (git-ignored)
```

---

## 🎯 Use Cases

### 📊 Market Research
```bash
"Analyze consumer sentiment about electric vehicles across Reddit"
```

### 🔬 Academic Research
```bash
"Research how Reddit communities discuss climate change solutions"
```

### 💼 Competitive Analysis
```bash
"What are developers saying about Next.js vs Remix?"
```

### 📈 Trend Discovery
```bash
"Find emerging AI tools being discussed on Reddit this week"
```

---

## 🔧 Advanced Configuration

### Environment Variables
```env
# Required
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret

# Optional
REDDIT_USER_AGENT=YourApp/1.0  # Customize user agent
```

### MCP Resources

Access comprehensive server documentation:

- 📖 `reddit://server-info` - Complete server capabilities, tools, prompts, and usage examples

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| 🔴 "Reddit API credentials not found" | Ensure `.env` file exists with valid credentials |
| ⏱️ Rate limit errors | Automatic retry after 60 seconds |
| 🚫 "Subreddit not found" | Check spelling (use "technology" not "r/technology") |
| 🔌 MCP connection failed | Verify full path in Claude Code command |

---

## 📚 Documentation

- 📖 [Architecture Overview](specs/agentic-discovery-architecture.md)
- 🤖 [Research Agent Details](specs/reddit-research-agent-spec.md)
- 🔍 [Deep Research Architecture](specs/deep-research-reddit-architecture.md)
- 🛠️ [API Reference](ai-docs/reddit-mcp-tools-reference.md)

---

## 🤝 Contributing

Contributions welcome! This project uses:
- 🐍 Python 3.11+ with type hints
- 📦 uv for package management
- 🚀 FastMCP for the server framework
- 🗄️ ChromaDB for vector search

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

<div align="center">
  
**Built with ❤️ for Reddit researchers and data enthusiasts**

[Report Issues](https://github.com/king-of-the-grackles/reddit-research-mcp/issues) • 
[Request Features](https://github.com/king-of-the-grackles/reddit-research-mcp/issues) • 
[Star on GitHub](https://github.com/king-of-the-grackles/reddit-research-mcp)

</div>