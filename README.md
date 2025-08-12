# Reddit MCP Server - MVP

A minimal Model Context Protocol (MCP) server that provides LLMs with access to Reddit content through three core tools. Built with FastMCP and PRAW for quick deployment.

## Features

- **Search Reddit**: Search across all of Reddit or specific subreddits
- **Fetch Subreddit Posts**: Get posts from any subreddit (hot, new, top, rising)
- **Fetch Comments**: Retrieve posts with their complete comment trees

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

```bash
uv run src/server.py
```

The server will start and be ready to accept MCP connections.

## Available Tools

### 1. search_reddit_tool

Search Reddit content with filtering options.

**Parameters:**
- `query` (required): Search query string
- `subreddit`: Limit search to specific subreddit
- `sort`: "relevance", "hot", "top", or "new" (default: "relevance")
- `time_filter`: "all", "year", "month", "week", or "day" (default: "all")
- `limit`: Maximum results, up to 100 (default: 25)

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

## Usage Examples

### Search for AI discussions
```python
search_reddit_tool(
    query="artificial intelligence",
    sort="top",
    time_filter="week",
    limit=10
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