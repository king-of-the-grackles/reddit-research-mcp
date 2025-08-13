from fastmcp import FastMCP
from typing import Optional, Literal, List, Union
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_reddit_client
from src.tools.search import search_all_reddit, search_in_subreddit
from src.tools.posts import fetch_subreddit_posts, fetch_multiple_subreddits
from src.tools.comments import fetch_submission_with_comments
from src.tools.discover import discover_subreddits
from src.resources import register_resources

# Initialize MCP server
mcp = FastMCP("Reddit MCP", instructions="""
Reddit MCP Server - Efficient Reddit Content Access

IMPORTANT: For best results, follow this workflow:
1. START by reading reddit://server-info for complete documentation
2. Use discover_subreddits_tool FIRST to find relevant communities
3. Batch operations when possible for efficiency

Quick Start: Try the 'get_started' prompt for interactive guidance.
""")

# Initialize Reddit client
reddit = get_reddit_client()

# Register resources
register_resources(mcp, reddit)


@mcp.tool()
def search_posts_tool(
    query: str,
    sort: Literal["relevance", "hot", "top", "new"] = "relevance",
    time_filter: Literal["all", "year", "month", "week", "day"] = "all",
    limit: int = 10
):
    """
    Search for posts across ALL of Reddit.
    
    Use this to find posts about any topic from anywhere on Reddit.
    For searching within a specific subreddit, use search_in_subreddit_tool instead.
    
    TIP: Consider using discover_subreddits_tool first to find relevant communities.
    
    Args:
        query: Search terms (e.g., "python tutorial", "machine learning news")
        sort: How to sort results (relevance, hot, top, new)
        time_filter: Time period to search (all, year, month, week, day)
        limit: Maximum number of results (max 100, default 10)
    
    Returns:
        Posts matching your search from across Reddit
    """
    return search_all_reddit(
        query=query,
        reddit=reddit,
        sort=sort,
        time_filter=time_filter,
        limit=limit
    )


@mcp.tool()
def search_in_subreddit_tool(
    subreddit_name: str,
    query: str,
    sort: Literal["relevance", "hot", "top", "new"] = "relevance",
    time_filter: Literal["all", "year", "month", "week", "day"] = "all",
    limit: int = 10
):
    """
    Search for posts within a SPECIFIC subreddit.
    
    Use this when you want to search for content in a known subreddit.
    If you don't know the subreddit name, use discover_subreddits_tool first.
    
    Args:
        subreddit_name: The subreddit to search in (e.g., "python", "MachineLearning")
        query: Search terms to find within that subreddit
        sort: How to sort results (relevance, hot, top, new)
        time_filter: Time period to search (all, year, month, week, day)
        limit: Maximum number of results (max 100, default 10)
    
    Returns:
        Posts matching your search from the specified subreddit
    """
    return search_in_subreddit(
        subreddit_name=subreddit_name,
        query=query,
        reddit=reddit,
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
    Browse the latest posts from a specific subreddit (no search).
    
    Use this to see what's currently popular/new in a subreddit.
    For searching within a subreddit, use search_in_subreddit_tool instead.
    
    Args:
        subreddit_name: Exact subreddit name (e.g., "python", "MachineLearning", "artificial")
                        Common AI subreddits: "artificial", "MachineLearning", "deeplearning",
                        "singularity", "OpenAI", "LocalLLaMA"
        listing_type: Type of posts to fetch (hot, new, top, rising)
        time_filter: Time period for top posts (all, year, month, week, day)
        limit: Maximum number of posts (max 100, default 10)
    
    Returns:
        Latest posts from the subreddit. If not found, use discover_subreddits_tool.
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
    query: Optional[str] = None,
    queries: Optional[Union[List[str], str]] = None,
    limit: int = 10,
    include_nsfw: bool = False
):
    """
    Discover subreddits by searching for keywords or topics. Supports batch queries!
    
    **RECOMMENDED FIRST STEP** - Use this tool FIRST when looking for subreddits. Batch mode is more efficient.
    
    Args:
        query: Single search term (e.g., "python", "gaming")
        queries: List of search terms for batch discovery - MORE EFFICIENT!
                 Example: ["django", "flask", "fastapi"] returns all results in one call
        limit: Maximum results per query (default 10)
        include_nsfw: Whether to include NSFW subreddits (default False)
    
    Returns:
        Single query: Subreddit list with metadata (has_more_results, suggestions)
        Batch queries: Results grouped by query term (reduces API calls by 70%+)
    
    Examples:
        Single: query="python" returns Python-related subreddits
        Batch: queries=["python", "django", "flask"] returns all in ONE response
        
    The response includes helpful metadata:
        - has_more_results: indicates if limit was reached
        - search_suggestions: alternative queries if few results found
        - total_found: shows impact of NSFW filtering
    
    IMPORTANT - Token Limits & Batch Strategy:
        MCP has a 25,000 token response limit. Large batch queries may exceed this.
        
        For comprehensive discovery (e.g., all gaming communities):
        - Use MULTIPLE smaller batches instead of one large batch
        - Safe: 5 queries with limit=10 each (uses ~3-5K tokens)
        - Risky: 10+ queries with limit=15 each (may exceed token limit)
        
        Example for comprehensive gaming discovery:
        - Call 1: queries=["gaming", "video games", "pc gaming", "console", "esports"]
        - Call 2: queries=["board games", "tabletop", "card games", "rpg", "chess"]  
        - Call 3: queries=["retro gaming", "arcade", "indie games", "mobile gaming"]
        
        This approach ensures complete results without token overflow errors.
    """
    # Handle string JSON input from MCP (convert to list)
    if queries and isinstance(queries, str):
        import json
        try:
            queries = json.loads(queries)
        except json.JSONDecodeError:
            # If it's not JSON, treat it as a single query
            queries = [queries]
    
    return discover_subreddits(
        query=query,
        queries=queries,
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
    
    **MORE EFFICIENT** than calling fetch_subreddit_posts_tool multiple times.
    
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


@mcp.prompt()
def get_started() -> str:
    """
    Welcome to Reddit MCP! Returns initial guidance for using this server effectively.
    """
    return """Welcome to Reddit MCP! To use this server effectively:

1. **First, read the server documentation**: Access the reddit://server-info resource for complete usage guidelines, best practices, and examples.

2. **Key capabilities**:
   - Search Reddit globally or within specific subreddits
   - Discover relevant subreddits using batch queries
   - Fetch posts and comments with efficient batch operations
   
3. **Best practices**:
   - Use discover_subreddits_tool FIRST to find relevant communities
   - Batch multiple queries together to reduce API calls
   - Use fetch_multiple_subreddits_tool for efficient multi-subreddit fetching

Start by reading reddit://server-info for detailed documentation and examples!"""


def main():
    """Main entry point for the Reddit MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()