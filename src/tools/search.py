from typing import Optional, Dict, Any, Literal
import praw
from prawcore import (
    NotFound,
    Forbidden,
    TooManyRequests,
    ServerError,
    ResponseException,
)
from fastmcp import Context
from ..models import SearchResult, RedditPost


def search_in_subreddit(
    subreddit_name: str,
    query: str,
    reddit: praw.Reddit,
    sort: Literal["relevance", "hot", "top", "new"] = "relevance",
    time_filter: Literal["all", "year", "month", "week", "day"] = "all",
    limit: int = 10,
    ctx: Context = None
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
        ctx: FastMCP context (auto-injected by decorator)

    Returns:
        Dictionary containing search results from the specified subreddit
    """
    # Phase 1: Accept context but don't use it yet

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
        except NotFound as e:
            return {
                "error": f"Subreddit r/{clean_name} not found",
                "status_code": 404,
                "recovery": "Use discover_subreddits to find valid communities"
            }
        except Forbidden as e:
            return {
                "error": f"Access to r/{clean_name} forbidden",
                "status_code": 403,
                "detail": e.response.text[:200] if hasattr(e, 'response') else None,
                "recovery": "Subreddit may be private, quarantined, or banned"
            }
        except TooManyRequests as e:
            return {
                "error": "Rate limited by Reddit API",
                "status_code": 429,
                "retry_after_seconds": e.retry_after if hasattr(e, 'retry_after') else None,
                "recovery": "Wait before retrying"
            }
        except ServerError as e:
            return {
                "error": "Reddit server error",
                "status_code": e.response.status_code if hasattr(e, 'response') else 500,
                "recovery": "Reddit is experiencing issues - retry after a short delay"
            }
        except ResponseException as e:
            return {
                "error": f"Reddit API error: {str(e)}",
                "status_code": e.response.status_code if hasattr(e, 'response') else None,
                "response_body": e.response.text[:300] if hasattr(e, 'response') else None,
                "recovery": "Check subreddit name and retry"
            }
        
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
        
    except TooManyRequests as e:
        return {
            "error": "Rate limited by Reddit API",
            "status_code": 429,
            "retry_after_seconds": e.retry_after if hasattr(e, 'retry_after') else None,
            "recovery": "Wait before retrying"
        }
    except ResponseException as e:
        return {
            "error": f"Reddit API error: {str(e)}",
            "status_code": e.response.status_code if hasattr(e, 'response') else None,
            "response_body": e.response.text[:300] if hasattr(e, 'response') else None,
            "recovery": "Check parameters and retry"
        }
    except Exception as e:
        return {
            "error": f"Search in subreddit failed: {str(e)}",
            "error_type": type(e).__name__,
            "recovery": "Check parameters match schema from get_operation_schema"
        }