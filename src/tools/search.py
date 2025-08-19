from typing import Optional, Dict, Any, Literal
import praw
from prawcore import NotFound, Forbidden
from ..models import SearchResult, RedditPost


def search_in_subreddit(
    subreddit_name: str,
    query: str,
    reddit: praw.Reddit,
    sort: Literal["relevance", "hot", "top", "new"] = "relevance",
    time_filter: Literal["all", "year", "month", "week", "day"] = "all",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Search for posts within a specific subreddit.
    
    Args:
        subreddit_name: Name of the subreddit to search in (required)
        query: Search query string
        reddit: Configured Reddit client
        sort: Sort method for results
        time_filter: Time filter for results
        limit: Maximum number of results (max 100, default 10)
    
    Returns:
        Dictionary containing search results from the specified subreddit
    """
    try:
        # Validate limit
        limit = min(max(1, limit), 100)
        
        # Clean subreddit name (remove r/ prefix if present)
        clean_name = subreddit_name.replace("r/", "").replace("/r/", "").strip()
        
        # Search within the specified subreddit
        try:
            subreddit_obj = reddit.subreddit(clean_name)
            # Verify subreddit exists
            _ = subreddit_obj.display_name
            
            search_results = subreddit_obj.search(
                query,
                sort=sort,
                time_filter=time_filter,
                limit=limit
            )
        except NotFound:
            return {
                "error": f"Subreddit r/{clean_name} not found",
                "suggestion": "discover_subreddits({'query': 'topic'})"
            }
        except Forbidden:
            return {"error": f"Access to r/{clean_name} forbidden (may be private)"}
        
        # Parse results
        results = []
        for submission in search_results:
            results.append(RedditPost(
                id=submission.id,
                title=submission.title,
                author=str(submission.author) if submission.author else "[deleted]",
                subreddit=submission.subreddit.display_name,
                score=submission.score,
                created_utc=submission.created_utc,
                url=submission.url,
                num_comments=submission.num_comments,
                permalink=f"https://reddit.com{submission.permalink}"
            ))
        
        result = SearchResult(
            results=results,
            count=len(results)
        )
        
        return result.model_dump()
        
    except Exception as e:
        return {"error": f"Search in subreddit failed: {str(e)}"}