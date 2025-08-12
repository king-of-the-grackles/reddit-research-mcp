from fastmcp import FastMCP
from typing import Optional, Literal, List
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_reddit_client
from src.tools.search import search_reddit
from src.tools.posts import fetch_subreddit_posts, fetch_multiple_subreddits
from src.tools.comments import fetch_submission_with_comments
from src.tools.discover import discover_subreddits
from src.resources import register_resources

# Initialize MCP server
mcp = FastMCP("Reddit MCP")

# Initialize Reddit client
reddit = get_reddit_client()

# Register resources
register_resources(mcp, reddit)


@mcp.tool()
def search_reddit_tool(
    query: str,
    subreddit: Optional[str] = None,
    sort: Literal["relevance", "hot", "top", "new"] = "relevance",
    time_filter: Literal["all", "year", "month", "week", "day"] = "all",
    limit: int = 10
):
    """
    Search Reddit content WITHIN posts across all of Reddit or a specific subreddit.
    
    NOTE: This searches inside post content, not for subreddit names.
    To find subreddits by topic, use discover_subreddits_tool instead.
    
    Args:
        query: Search query string (searches in post titles and content)
        subreddit: Optional subreddit name to limit search (e.g., "python", "MachineLearning")
        sort: How to sort results (relevance, hot, top, new)
        time_filter: Time period to search (all, year, month, week, day)
        limit: Maximum number of results to return (max 100, default 10)
    
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
    limit: int = 10
):
    """
    Get posts from a specific subreddit.
    
    Args:
        subreddit_name: Name of the subreddit - use exact name like "python", "MachineLearning", 
                        "artificial" (NOT "r/python" or "artificialintelligence")
                        Common AI subreddits: "artificial", "MachineLearning", "deeplearning",
                        "singularity", "OpenAI", "LocalLLaMA"
        listing_type: Type of posts to fetch (hot, new, top, rising)
        time_filter: Time period for top posts (all, year, month, week, day)
        limit: Maximum number of posts to return (max 100, default 10)
    
    Returns:
        Posts from the subreddit with metadata.
        If subreddit not found, use discover_subreddits_tool to find valid names.
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


@mcp.tool()
def discover_subreddits_tool(
    query: str,
    limit: int = 10,
    include_nsfw: bool = False
):
    """
    Discover subreddits by searching for a keyword or topic.
    
    Use this tool FIRST when looking for subreddits about a specific topic.
    Returns subreddit names that can be used with other tools.
    
    Args:
        query: Search term to find subreddits (e.g., "artificial intelligence", "python", "gaming")
        limit: Maximum number of results (default 10)
        include_nsfw: Whether to include NSFW subreddits (default False)
    
    Returns:
        List of matching subreddits with names, descriptions, and subscriber counts.
        Use the exact 'name' field from results when calling other tools.
    
    Example:
        Query "machine learning" might return subreddits like "MachineLearning", 
        "learnmachinelearning", "deeplearning", etc.
    """
    return discover_subreddits(
        query=query,
        reddit=reddit,
        limit=limit,
        include_nsfw=include_nsfw
    )


@mcp.tool()
def fetch_multiple_subreddits_tool(
    subreddit_names: List[str],
    listing_type: Literal["hot", "new", "top", "rising"] = "hot",
    time_filter: Optional[Literal["all", "year", "month", "week", "day"]] = None,
    limit_per_subreddit: int = 5
):
    """
    Fetch posts from multiple subreddits in a single efficient call.
    
    This is more efficient than calling fetch_subreddit_posts_tool multiple times.
    
    Args:
        subreddit_names: List of subreddit names (e.g., ["python", "MachineLearning", "artificial"])
        listing_type: Type of posts to fetch (hot, new, top, rising)
        time_filter: Time period for top posts (all, year, month, week, day)
        limit_per_subreddit: Maximum posts per subreddit (max 25, default 5)
    
    Returns:
        Posts grouped by subreddit. More efficient than multiple individual calls.
    
    Example:
        subreddit_names=["MachineLearning", "deeplearning", "artificial"] fetches 
        posts from all three subreddits in one API call.
    """
    return fetch_multiple_subreddits(
        subreddit_names=subreddit_names,
        reddit=reddit,
        listing_type=listing_type,
        time_filter=time_filter,
        limit_per_subreddit=limit_per_subreddit
    )


def main():
    """Main entry point for the Reddit MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()