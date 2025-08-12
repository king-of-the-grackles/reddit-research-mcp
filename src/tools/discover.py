"""Subreddit discovery tools for finding and validating subreddits."""

import praw
from typing import Dict, List, Any, Optional


def discover_subreddits(
    query: str,
    reddit: praw.Reddit,
    limit: int = 10,
    include_nsfw: bool = False
) -> Dict[str, Any]:
    """
    Search for subreddits by keyword or topic.
    
    Args:
        query: Search term to find subreddits
        reddit: Reddit instance
        limit: Maximum number of results (default 10)
        include_nsfw: Whether to include NSFW subreddits (default False)
    
    Returns:
        Dictionary with discovered subreddits and their metadata
    """
    try:
        results = []
        
        # Search for subreddits matching the query
        for subreddit in reddit.subreddits.search(query, limit=limit):
            # Skip NSFW subreddits if not requested
            if subreddit.over18 and not include_nsfw:
                continue
                
            try:
                # Validate subreddit exists and is accessible
                _ = subreddit.id  # This will fail if subreddit doesn't exist
                
                results.append({
                    "name": subreddit.display_name,
                    "title": subreddit.title,
                    "description": subreddit.public_description[:200] if subreddit.public_description else "",
                    "subscribers": subreddit.subscribers,
                    "over_18": subreddit.over18,
                    "url": f"https://reddit.com/r/{subreddit.display_name}",
                    "created_utc": subreddit.created_utc
                })
            except Exception:
                # Skip inaccessible subreddits
                continue
        
        return {
            "query": query,
            "count": len(results),
            "subreddits": results,
            "tip": "Use the exact 'name' field when calling other tools (e.g., 'MachineLearning' not 'r/MachineLearning')"
        }
        
    except Exception as e:
        return {
            "error": f"Failed to search for subreddits: {str(e)}",
            "query": query,
            "subreddits": []
        }


def validate_subreddit(
    subreddit_name: str,
    reddit: praw.Reddit
) -> Dict[str, Any]:
    """
    Validate if a subreddit exists and return its info.
    
    Args:
        subreddit_name: Name of the subreddit to validate
        reddit: Reddit instance
    
    Returns:
        Dictionary with validation result and subreddit info if valid
    """
    # Clean the subreddit name
    clean_name = subreddit_name.replace("r/", "").replace("/r/", "").strip()
    
    try:
        subreddit = reddit.subreddit(clean_name)
        # Try to access an attribute to verify it exists
        _ = subreddit.id
        
        return {
            "valid": True,
            "name": subreddit.display_name,
            "subscribers": subreddit.subscribers,
            "is_private": subreddit.subreddit_type == "private",
            "over_18": subreddit.over18
        }
    except Exception:
        return {
            "valid": False,
            "name": clean_name,
            "error": f"Subreddit '{clean_name}' not found or inaccessible",
            "suggestion": "Use discover_subreddits_tool to find valid subreddit names"
        }