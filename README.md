# Reddit MCP Server

A Model Context Protocol (MCP) server that provides LLMs with comprehensive access to Reddit content through six powerful tools and three MCP resources. Built with FastMCP and PRAW for quick deployment.

## Features

- **Search Reddit**: Search across all of Reddit or within specific subreddits
- **Discover Subreddits**: Find relevant subreddits by topic with confidence scoring
- **Fetch Posts**: Get posts from single or multiple subreddits efficiently
- **Fetch Comments**: Retrieve posts with their complete comment trees
- **MCP Resources**: Access popular subreddits, subreddit info, and server capabilities

## Quick Start

### Prerequisites

- Python 3.11+
- Reddit API credentials ([Get them here](https://www.reddit.com/prefs/apps))
  1. Go to https://www.reddit.com/prefs/apps
  2. Click "Create App" or "Create Another App"
  3. Choose "script" as the app type
  4. Note your `client_id` (under "personal use script") and `client_secret`

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd reddit-mcp-poc
```

2. Install dependencies using uv:
```bash
pip install uv
uv sync
```

### Configuration

Create a `.env` file in the project root:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=RedditMCP/1.0 by u/your_username
```

### Running the Server

#### Production Mode
```bash
uv run src/server.py
```

#### Development Mode (with MCP Inspector)
```bash
fastmcp dev src/server.py
```

The server will start and be ready to accept MCP connections.

## Available Tools

### 1. search_posts_tool

Search for posts across all of Reddit.

**Parameters:**
- `query` (required): Search query string
- `sort`: "relevance", "hot", "top", or "new" (default: "relevance")
- `time_filter`: "all", "year", "month", "week", or "day" (default: "all")
- `limit`: Maximum results, up to 100 (default: 10)

### 2. fetch_subreddit_posts_tool

Get posts from a specific subreddit.

**Parameters:**
- `subreddit_name` (required): Subreddit name (without r/ prefix)
- `listing_type`: "hot", "new", "top", or "rising" (default: "hot")
- `time_filter`: For top posts - "all", "year", "month", "week", or "day"
- `limit`: Maximum posts, up to 100 (default: 25)

### 3. fetch_submission_with_comments_tool

Retrieve a Reddit post with its comment tree.

**Parameters:**
- `submission_id` OR `url`: Reddit post ID or full URL
- `comment_limit`: Maximum comments to fetch (default: 100)
- `comment_sort`: "best", "top", or "new" (default: "best")

### 4. search_in_subreddit_tool

Search for posts within a specific subreddit.

**Parameters:**
- `subreddit_name` (required): The subreddit to search in (without r/ prefix)
- `query` (required): Search query string
- `sort`: "relevance", "hot", "top", or "new" (default: "relevance")
- `time_filter`: "all", "year", "month", "week", or "day" (default: "all")
- `limit`: Maximum results, up to 100 (default: 10)

### 5. discover_subreddits_tool

Discover subreddits by searching for keywords or topics. Supports batch queries for efficiency.

**Parameters:**
- `query`: Single search term (e.g., "python", "gaming")
- `queries`: List of search terms for batch discovery (more efficient!)
- `limit`: Maximum results per query (default: 10)
- `include_nsfw`: Whether to include NSFW subreddits (default: False)

**Features:**
- Confidence scoring based on name match, description, and activity
- Batch mode reduces API calls significantly
- Returns metadata including has_more_results and search suggestions

### 6. fetch_multiple_subreddits_tool

Fetch posts from multiple subreddits in a single efficient call.

**Parameters:**
- `subreddit_names` (required): List of subreddit names
- `listing_type`: "hot", "new", "top", or "rising" (default: "hot")
- `time_filter`: For top posts - "all", "year", "month", "week", or "day"
- `limit_per_subreddit`: Maximum posts per subreddit (max 25, default: 5)

## MCP Resources

The server provides three MCP resources for accessing commonly used data:

### 1. reddit://popular-subreddits
Returns a list of the 25 most popular subreddits with subscriber counts and descriptions.

### 2. reddit://subreddit/{name}/about
Get detailed information about a specific subreddit including:
- Title and description
- Subscriber count and active users
- Subreddit rules
- Creation date and other metadata

### 3. reddit://server-info
Returns comprehensive information about the MCP server including:
- Available tools and resources
- Version information
- Usage examples
- Current rate limit status

## Usage Examples

### Search for AI discussions across Reddit
```python
search_posts_tool(
    query="artificial intelligence",
    sort="top",
    time_filter="week",
    limit=10
)
```

### Search within a specific subreddit
```python
search_in_subreddit_tool(
    subreddit_name="MachineLearning",
    query="transformers",
    sort="relevance",
    limit=15
)
```

### Discover relevant subreddits
```python
# Single query
discover_subreddits_tool(
    query="python",
    limit=10,
    include_nsfw=False
)

# Batch queries (more efficient!)
discover_subreddits_tool(
    queries=["django", "flask", "fastapi"],
    limit=5
)
```

### Get latest posts from r/technology
```python
fetch_subreddit_posts_tool(
    subreddit_name="technology",
    listing_type="new",
    limit=20
)
```

### Fetch from multiple subreddits at once
```python
fetch_multiple_subreddits_tool(
    subreddit_names=["python", "django", "flask"],
    listing_type="hot",
    limit_per_subreddit=5
)
```

### Fetch a post with comments
```python
fetch_submission_with_comments_tool(
    url="https://reddit.com/r/programming/comments/...",
    comment_limit=50,
    comment_sort="best"
)
```

## Testing

Run the test suite:
```bash
uv run pytest tests/
```

## Project Structure

```
reddit-mcp-poc/
├── src/
│   ├── server.py           # Main MCP server
│   ├── config.py           # Reddit client configuration
│   ├── models.py           # Pydantic data models
│   └── tools/              # Tool implementations
│       ├── search.py       # Search functionality
│       ├── posts.py        # Subreddit posts fetching
│       └── comments.py     # Comments fetching
├── tests/
│   └── test_tools.py       # Unit tests
├── pyproject.toml          # Project dependencies
├── .env                    # Your API credentials
└── README.md              # This file
```

## Error Handling

The server handles common Reddit API errors gracefully:
- **Rate Limiting**: Automatically handled by PRAW with 5-minute cooldown
- **Not Found**: Returns error message for non-existent subreddits/posts
- **Forbidden**: Returns error message for private/restricted content
- **Invalid Input**: Validates and sanitizes all input parameters

## Limitations

This MVP implementation has some intentional limitations:
- Read-only access (no posting, commenting, or voting)
- No user authentication (uses application-only auth)
- Limited comment expansion (doesn't fetch "more comments")
- No caching (each request hits Reddit API directly)

## Next Steps

Once the MVP is working, consider:
1. Add user authentication for write operations
2. Implement caching for better performance
3. Add more specialized tools (user profiles, search by flair, etc.)
4. Create MCP resources for saved queries
5. Add analytics and metrics tools

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Reddit API credentials not found" | Ensure `.env` file exists with valid credentials |
| Rate limit errors | Wait a few minutes; PRAW handles this automatically |
| "Subreddit not found" | Verify subreddit name (without r/ prefix) |
| No search results | Try broader search terms or different time filter |
| Import errors | Run `uv sync` to install all dependencies |

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.