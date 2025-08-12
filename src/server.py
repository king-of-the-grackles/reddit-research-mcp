from fastmcp import FastMCP
from typing import Optional, Literal
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_reddit_client
from src.tools.search import search_reddit
from src.tools.posts import fetch_subreddit_posts
from src.tools.comments import fetch_submission_with_comments

# Initialize MCP server
mcp = FastMCP("Reddit MCP")

# Initialize Reddit client
reddit = get_reddit_client()


@mcp.tool()
def search_reddit_tool(
    query: str,
    subreddit: Optional[str] = None,
    sort: Literal["relevance", "hot", "top", "new"] = "relevance",
    time_filter: Literal["all", "year", "month", "week", "day"] = "all",
    limit: int = 25
):
    """
    Search Reddit content across all of Reddit or within a specific subreddit.
    
    Args:
        query: Search query string
        subreddit: Optional subreddit name to limit search (without r/ prefix)
        sort: How to sort results (relevance, hot, top, new)
        time_filter: Time period to search (all, year, month, week, day)
        limit: Maximum number of results to return (max 100, default 25)
    
    Returns:
        Search results with post metadata
    """
    return search_reddit(
        query=query,
        reddit=reddit,
        subreddit=subreddit,
        sort=sort,
        time_filter=time_filter,
        limit=limit
    )


@mcp.tool()
def fetch_subreddit_posts_tool(
    subreddit_name: str,
    listing_type: Literal["hot", "new", "top", "rising"] = "hot",
    time_filter: Optional[Literal["all", "year", "month", "week", "day"]] = None,
    limit: int = 25
):
    """
    Get posts from a specific subreddit.
    
    Args:
        subreddit_name: Name of the subreddit (without r/ prefix)
        listing_type: Type of posts to fetch (hot, new, top, rising)
        time_filter: Time period for top posts (all, year, month, week, day)
        limit: Maximum number of posts to return (max 100, default 25)
    
    Returns:
        Posts from the subreddit with metadata
    """
    return fetch_subreddit_posts(
        subreddit_name=subreddit_name,
        reddit=reddit,
        listing_type=listing_type,
        time_filter=time_filter,
        limit=limit
    )


@mcp.tool()
def fetch_submission_with_comments_tool(
    submission_id: Optional[str] = None,
    url: Optional[str] = None,
    comment_limit: int = 100,
    comment_sort: Literal["best", "top", "new"] = "best"
):
    """
    Get a Reddit post with its comment tree.
    
    Args:
        submission_id: Reddit post ID (e.g., "1abc234")
        url: Full URL to the Reddit post (alternative to submission_id)
        comment_limit: Maximum number of comments to fetch (default 100)
        comment_sort: How to sort comments (best, top, new)
    
    Returns:
        Post content with nested comment tree
    """
    return fetch_submission_with_comments(
        reddit=reddit,
        submission_id=submission_id,
        url=url,
        comment_limit=comment_limit,
        comment_sort=comment_sort
    )


def main():
    """Main entry point for the Reddit MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()