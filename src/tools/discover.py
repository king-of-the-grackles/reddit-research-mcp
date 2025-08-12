"""Subreddit discovery tools for finding and validating subreddits."""

import praw
from typing import Dict, List, Any, Optional


def discover_subreddits(
    query: Optional[str] = None,
    queries: Optional[List[str]] = None,
    reddit: praw.Reddit = None,
    limit: int = 10,
    include_nsfw: bool = False
) -> Dict[str, Any]:
    """
    Search for subreddits by keyword or topic. Supports batch queries.
    
    Args:
        query: Single search term to find subreddits
        queries: List of search terms for batch discovery (more efficient)
        reddit: Reddit instance
        limit: Maximum number of results per query (default 10)
        include_nsfw: Whether to include NSFW subreddits (default False)
    
    Returns:
        Dictionary with discovered subreddits and their metadata
    """
    # Handle batch queries
    if queries:
        batch_results = {}
        total_api_calls = 0
        
        for search_query in queries:
            result = _search_single_query(
                search_query, reddit, limit, include_nsfw
            )
            batch_results[search_query] = result
            total_api_calls += 1
        
        return {
            "batch_mode": True,
            "total_queries": len(queries),
            "api_calls_made": total_api_calls,
            "results": batch_results,
            "tip": "Batch mode reduces API calls. Use the exact 'name' field when calling other tools."
        }
    
    # Handle single query
    elif query:
        return _search_single_query(query, reddit, limit, include_nsfw)
    
    else:
        return {
            "error": "Either 'query' or 'queries' parameter must be provided",
            "subreddits": []
        }


def _search_single_query(
    query: str,
    reddit: praw.Reddit,
    limit: int,
    include_nsfw: bool
) -> Dict[str, Any]:
    """Internal function to search for a single query."""
    try:
        results = []
        total_found = 0
        nsfw_filtered = 0
        
        # Search for subreddits matching the query
        # Fetch extra to account for NSFW filtering
        fetch_limit = limit * 2 if not include_nsfw else limit
        
        for subreddit in reddit.subreddits.search(query, limit=fetch_limit):
            total_found += 1
            
            # Skip NSFW subreddits if not requested
            if subreddit.over18 and not include_nsfw:
                nsfw_filtered += 1
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
                
                # Stop when we have enough results
                if len(results) >= limit:
                    break
                    
            except Exception:
                # Skip inaccessible subreddits
                continue
        
        # Determine if more results might be available
        has_more_results = total_found >= fetch_limit
        
        # Generate search suggestions if few results
        search_suggestions = []
        if len(results) < 3:
            # Suggest related terms based on the query
            if " " not in query:
                # Single word - suggest variations
                search_suggestions = [
                    f"{query} community",
                    f"{query}s",  # plural
                    f"learn{query}"
                ]
            else:
                # Multi-word - suggest individual words
                words = query.split()
                search_suggestions = words[:3]  # First 3 words as separate searches
        
        response = {
            "query": query,
            "count": len(results),
            "total_found": total_found,
            "nsfw_filtered": nsfw_filtered,
            "has_more_results": has_more_results,
            "subreddits": results,
            "tip": "Use the exact 'name' field when calling other tools (e.g., 'MachineLearning' not 'r/MachineLearning')"
        }
        
        # Only add suggestions if there are any
        if search_suggestions:
            response["search_suggestions"] = search_suggestions
        
        return response
        
    except Exception as e:
        return {
            "error": f"Failed to search for subreddits: {str(e)}",
            "query": query,
            "subreddits": [],
            "count": 0,
            "has_more_results": False
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