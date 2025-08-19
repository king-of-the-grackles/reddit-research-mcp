from typing import Optional, Dict, Any, Literal, List
import praw
from prawcore import NotFound, Forbidden
from ..models import SubredditPostsResult, RedditPost, SubredditInfo


def fetch_subreddit_posts(
    subreddit_name: str,
    reddit: praw.Reddit,
    listing_type: Literal["hot", "new", "top", "rising"] = "hot",
    time_filter: Optional[Literal["all", "year", "month", "week", "day"]] = None,
    limit: int = 25
) -> Dict[str, Any]:
    """
    Fetch posts from a specific subreddit.
    
    Args:
        subreddit_name: Name of the subreddit (without r/ prefix)
        reddit: Configured Reddit client
        listing_type: Type of listing to fetch
        time_filter: Time filter for top posts
        limit: Maximum number of posts (max 100)
    
    Returns:
        Dictionary containing posts and subreddit info
    """
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
        except NotFound:
            return {
                "error": f"Subreddit r/{clean_name} not found",
                "suggestion": "discover_subreddits({'query': 'topic'})"
            }
        except Forbidden:
            return {"error": f"Access to r/{clean_name} forbidden (may be private)"}
        
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
        
    except Exception as e:
        return {"error": f"Failed to fetch posts: {str(e)}"}


def fetch_multiple_subreddits(
    subreddit_names: List[str],
    reddit: praw.Reddit,
    listing_type: Literal["hot", "new", "top", "rising"] = "hot",
    time_filter: Optional[Literal["all", "year", "month", "week", "day"]] = None,
    limit_per_subreddit: int = 5
) -> Dict[str, Any]:
    """
    Fetch posts from multiple subreddits in a single call.
    
    Args:
        subreddit_names: List of subreddit names to fetch from
        reddit: Configured Reddit client
        listing_type: Type of listing to fetch
        time_filter: Time filter for top posts
        limit_per_subreddit: Maximum posts per subreddit (max 25)
    
    Returns:
        Dictionary containing posts from all requested subreddits
    """
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
            for submission in submissions:
                subreddit_name = submission.subreddit.display_name
                
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
            
            return {
                "subreddits_requested": clean_names,
                "subreddits_found": list(posts_by_subreddit.keys()),
                "posts_by_subreddit": posts_by_subreddit,
                "total_posts": sum(len(posts) for posts in posts_by_subreddit.values())
            }
            
        except Exception as e:
            return {
                "error": f"Failed to fetch from multiple subreddits: {str(e)}",
                "suggestion": "discover_subreddits({'query': 'topic'}) to find valid names"
            }
        
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}"}