from typing import Optional, Dict, Any, Literal
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
        
        # Get subreddit
        try:
            subreddit = reddit.subreddit(subreddit_name)
            # Force fetch to check if subreddit exists
            _ = subreddit.display_name
        except NotFound:
            return {"error": f"Subreddit r/{subreddit_name} not found"}
        except Forbidden:
            return {"error": f"Access to r/{subreddit_name} forbidden (may be private)"}
        
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