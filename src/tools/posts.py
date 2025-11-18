from typing import Optional, Dict, Any, Literal, List
import praw
from prawcore import (
    NotFound,
    Forbidden,
    TooManyRequests,
    ServerError,
    BadRequest,
    ResponseException,
)
from fastmcp import Context
from ..models import SubredditPostsResult, RedditPost, SubredditInfo


def fetch_subreddit_posts(
    subreddit_name: str,
    reddit: praw.Reddit,
    listing_type: Literal["hot", "new", "top", "rising"] = "hot",
    time_filter: Optional[Literal["all", "year", "month", "week", "day"]] = None,
    limit: int = 25,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Fetch posts from a specific subreddit.

    Args:
        subreddit_name: Name of the subreddit (without r/ prefix)
        reddit: Configured Reddit client
        listing_type: Type of listing to fetch
        time_filter: Time filter for top posts
        limit: Maximum number of posts (max 100)
        ctx: FastMCP context (auto-injected by decorator)

    Returns:
        Dictionary containing posts and subreddit info
    """
    # Phase 1: Accept context but don't use it yet

    try:
        # Validate limit
        limit = min(max(1, limit), 100)
        
        # Clean subreddit name (remove r/ prefix if present)
        clean_name = subreddit_name.replace("r/", "").replace("/r/", "").strip()
        
        # Get subreddit
        try:
            subreddit = reddit.subreddit(clean_name)
            # Force fetch to check if subreddit exists
            _ = subreddit.display_name
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
                "message": e.message if hasattr(e, 'message') else str(e),
                "recovery": f"Wait before retrying"
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
        
        # Get posts based on listing type
        if listing_type == "hot":
            submissions = subreddit.hot(limit=limit)
        elif listing_type == "new":
            submissions = subreddit.new(limit=limit)
        elif listing_type == "rising":
            submissions = subreddit.rising(limit=limit)
        elif listing_type == "top":
            # Use time_filter for top posts
            time_filter = time_filter or "all"
            submissions = subreddit.top(time_filter=time_filter, limit=limit)
        else:
            return {"error": f"Invalid listing_type: {listing_type}"}
        
        # Parse posts
        posts = []
        for submission in submissions:
            posts.append(RedditPost(
                id=submission.id,
                title=submission.title,
                selftext=submission.selftext if submission.selftext else None,
                author=str(submission.author) if submission.author else "[deleted]",
                subreddit=submission.subreddit.display_name,
                score=submission.score,
                upvote_ratio=submission.upvote_ratio,
                num_comments=submission.num_comments,
                created_utc=submission.created_utc,
                url=submission.url,
                permalink=f"https://reddit.com{submission.permalink}"
            ))
        
        # Get subreddit info
        subreddit_info = SubredditInfo(
            name=subreddit.display_name,
            subscribers=subreddit.subscribers,
            description=subreddit.public_description or ""
        )
        
        result = SubredditPostsResult(
            posts=posts,
            subreddit=subreddit_info,
            count=len(posts)
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
            "error": f"Failed to fetch posts: {str(e)}",
            "error_type": type(e).__name__,
            "recovery": "Check parameters match schema from get_operation_schema"
        }


async def fetch_multiple_subreddits(
    subreddit_names: List[str],
    reddit: praw.Reddit,
    listing_type: Literal["hot", "new", "top", "rising"] = "hot",
    time_filter: Optional[Literal["all", "year", "month", "week", "day"]] = None,
    limit_per_subreddit: int = 5,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Fetch posts from multiple subreddits in a single call.

    Args:
        subreddit_names: List of subreddit names to fetch from
        reddit: Configured Reddit client
        listing_type: Type of listing to fetch
        time_filter: Time filter for top posts
        limit_per_subreddit: Maximum posts per subreddit (max 25)
        ctx: FastMCP context (auto-injected by decorator)

    Returns:
        Dictionary containing posts from all requested subreddits
    """
    # Phase 1: Accept context but don't use it yet

    try:
        # Validate limit
        limit_per_subreddit = min(max(1, limit_per_subreddit), 25)
        
        # Clean subreddit names and join with +
        clean_names = [name.replace("r/", "").replace("/r/", "").strip() for name in subreddit_names]
        multi_subreddit_str = "+".join(clean_names)
        
        # Get combined subreddit
        try:
            multi_subreddit = reddit.subreddit(multi_subreddit_str)
            # Calculate total limit (max 100)
            total_limit = min(limit_per_subreddit * len(clean_names), 100)
            
            # Get posts based on listing type
            if listing_type == "hot":
                submissions = multi_subreddit.hot(limit=total_limit)
            elif listing_type == "new":
                submissions = multi_subreddit.new(limit=total_limit)
            elif listing_type == "rising":
                submissions = multi_subreddit.rising(limit=total_limit)
            elif listing_type == "top":
                time_filter = time_filter or "all"
                submissions = multi_subreddit.top(time_filter=time_filter, limit=total_limit)
            else:
                return {"error": f"Invalid listing_type: {listing_type}"}
            
            # Parse posts and group by subreddit
            posts_by_subreddit = {}
            processed_subreddits = set()

            for submission in submissions:
                subreddit_name = submission.subreddit.display_name

                # Report progress when encountering a new subreddit
                if subreddit_name not in processed_subreddits:
                    processed_subreddits.add(subreddit_name)
                    if ctx:
                        await ctx.report_progress(
                            progress=len(processed_subreddits),
                            total=len(clean_names),
                            message=f"Fetching r/{subreddit_name}"
                        )

                if subreddit_name not in posts_by_subreddit:
                    posts_by_subreddit[subreddit_name] = []

                # Only add up to limit_per_subreddit posts per subreddit
                if len(posts_by_subreddit[subreddit_name]) < limit_per_subreddit:
                    posts_by_subreddit[subreddit_name].append({
                        "id": submission.id,
                        "title": submission.title,
                        "author": str(submission.author) if submission.author else "[deleted]",
                        "score": submission.score,
                        "num_comments": submission.num_comments,
                        "created_utc": submission.created_utc,
                        "url": submission.url,
                        "permalink": f"https://reddit.com{submission.permalink}"
                    })
            
            found_names = list(posts_by_subreddit.keys())
            missing_names = [name for name in clean_names
                           if name.lower() not in [k.lower() for k in found_names]]

            return {
                "subreddits_requested": clean_names,
                "subreddits_found": found_names,
                "subreddits_failed": missing_names,
                "failure_reasons": {
                    name: "No posts returned (may be private, banned, empty, or misspelled)"
                    for name in missing_names
                } if missing_names else {},
                "posts_by_subreddit": posts_by_subreddit,
                "total_posts": sum(len(posts) for posts in posts_by_subreddit.values()),
                "success_rate": f"{len(found_names)}/{len(clean_names)}"
            }

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
                "recovery": "Check subreddit names and retry"
            }
        except Exception as e:
            return {
                "error": f"Failed to fetch from multiple subreddits: {str(e)}",
                "error_type": type(e).__name__,
                "recovery": "Use discover_subreddits to find valid community names"
            }

    except Exception as e:
        return {
            "error": f"Failed to process request: {str(e)}",
            "error_type": type(e).__name__,
            "recovery": "Check parameters match schema from get_operation_schema"
        }