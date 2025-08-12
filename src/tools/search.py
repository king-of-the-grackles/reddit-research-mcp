from typing import Optional, Dict, Any, Literal
import praw
from prawcore import NotFound, Forbidden
from ..models import SearchResult, RedditPost


def search_reddit(
    query: str,
    reddit: praw.Reddit,
    subreddit: Optional[str] = None,
    sort: Literal["relevance", "hot", "top", "new"] = "relevance",
    time_filter: Literal["all", "year", "month", "week", "day"] = "all",
    limit: int = 25
) -> Dict[str, Any]:
    """
    Search Reddit content.
    
    Args:
        query: Search query string
        reddit: Configured Reddit client
        subreddit: Optional subreddit to limit search to
        sort: Sort method for results
        time_filter: Time filter for results
        limit: Maximum number of results (max 100)
    
    Returns:
        Dictionary containing search results
    """
    try:
        # Validate limit
        limit = min(max(1, limit), 100)
        
        # Perform search
        if subreddit:
            try:
                subreddit_obj = reddit.subreddit(subreddit)
                search_results = subreddit_obj.search(
                    query,
                    sort=sort,
                    time_filter=time_filter,
                    limit=limit
                )
            except NotFound:
                return {"error": f"Subreddit r/{subreddit} not found"}
            except Forbidden:
                return {"error": f"Access to r/{subreddit} forbidden"}
        else:
            search_results = reddit.subreddit("all").search(
                query,
                sort=sort,
                time_filter=time_filter,
                limit=limit
            )
        
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
                num_comments=submission.num_comments
            ))
        
        result = SearchResult(
            results=results,
            count=len(results)
        )
        
        return result.model_dump()
        
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}