"""Subreddit discovery tools for finding and validating subreddits."""

import praw
import re
import math
import json
from typing import Dict, List, Any, Optional, Union


def calculate_name_match_score(subreddit_name: str, query: str) -> float:
    """Calculate how well the subreddit name matches the query."""
    name_lower = subreddit_name.lower()
    query_lower = query.lower()
    
    # Exact match = 1.0
    if name_lower == query_lower:
        return 1.0
    
    # Query is entire word in compound name
    name_parts = name_lower.replace('_', ' ').replace('-', ' ').split()
    if query_lower in name_parts:
        # e.g., "python" in "learn_python" = 0.8
        return 0.8
    
    # Query at start of name  
    if name_lower.startswith(query_lower):
        # e.g., "python" in "pythontips" = 0.7
        return 0.7
    
    # Query at end of name
    if name_lower.endswith(query_lower):
        # e.g., "python" in "learnpython" = 0.6
        return 0.6
    
    # Query anywhere in name
    if query_lower in name_lower:
        # Penalize by how much extra content there is
        ratio = len(query_lower) / len(name_lower)
        return min(0.5 * ratio, 0.4)
    
    return 0.0


def calculate_description_score(description: str, query: str) -> float:
    """Score based on query presence in description."""
    if not description:
        return 0.0
    
    desc_lower = description.lower()
    query_lower = query.lower()
    
    # Count occurrences (capped)
    occurrences = min(desc_lower.count(query_lower), 3)
    
    # Check if query appears as whole word
    whole_word_pattern = r'\b' + re.escape(query_lower) + r'\b'
    whole_word_matches = len(re.findall(whole_word_pattern, desc_lower))
    
    # Calculate score
    occurrence_score = occurrences * 0.2  # Max 0.6
    whole_word_bonus = min(whole_word_matches * 0.2, 0.4)
    
    return min(occurrence_score + whole_word_bonus, 1.0)


def calculate_activity_score(subscribers: int) -> float:
    """Score based on community size and activity."""
    if not subscribers or subscribers <= 0:
        return 0.0
    
    # Logarithmic scale for subscribers
    # log scale: 1K=0.3, 10K=0.4, 100K=0.5, 1M=0.6, 10M=0.7
    subscriber_score = min(math.log10(subscribers + 1) / 10, 0.7)
    
    # Activity bonus for larger communities
    activity_bonus = 0.3 if subscriber_score > 0.3 else 0.0
    
    return min(subscriber_score + activity_bonus, 1.0)


def calculate_penalties(subreddit_name: str, query: str) -> float:
    """Apply penalties for likely false positives."""
    penalty = 0.0
    name_lower = subreddit_name.lower()
    query_lower = query.lower()
    
    # Penalty for completely unrelated compound words
    if query_lower in name_lower and name_lower != query_lower:
        # Check if it's a compound word that changes meaning
        parts = name_lower.split(query_lower)
        prefix = parts[0] if parts else ""
        suffix = parts[-1] if len(parts) > 1 else ""
        
        # Common modifiers that suggest different topic
        topic_changers = ['ball', 'monty', 'royal', 'carpet', 'green']
        if any(mod in prefix + suffix for mod in topic_changers):
            penalty += 0.5
    
    # Generic/mega subreddit penalty
    generic_subs = ['funny', 'pics', 'videos', 'gifs', 'todayilearned', 'memes', 
                    'news', 'worldnews', 'politics', 'aww', 'music', 'movies']
    if name_lower in generic_subs:
        penalty += 0.7
    
    return penalty


def calculate_confidence(subreddit, query: str) -> Dict[str, Any]:
    """Calculate overall confidence score for a search result."""
    
    # Get individual scores
    name_score = calculate_name_match_score(subreddit.display_name, query)
    desc_score = calculate_description_score(subreddit.public_description or "", query)
    activity_score = calculate_activity_score(subreddit.subscribers)
    
    # Weighted combination based on match type
    if name_score >= 0.8:  # Strong name match
        # Name match is most important
        confidence = (
            name_score * 0.6 +      # 60% weight on name
            activity_score * 0.25 +  # 25% weight on activity
            desc_score * 0.15        # 15% weight on description
        )
        match_type = "exact_match" if name_score == 1.0 else "strong_match"
        
    elif name_score > 0:  # Partial name match
        # Balance between name and activity
        confidence = (
            name_score * 0.5 +      # 50% weight on name
            activity_score * 0.3 +  # 30% weight on activity
            desc_score * 0.2        # 20% weight on description
        )
        match_type = "partial_match"
        
    else:  # Description only match
        # Activity becomes more important for description-only matches
        confidence = (
            desc_score * 0.4 +      # 40% weight on description
            activity_score * 0.6     # 60% weight on activity
        )
        match_type = "description_only"
    
    # Apply penalties for suspicious patterns
    penalty = calculate_penalties(subreddit.display_name, query)
    confidence = max(0, confidence - penalty)
    
    return {
        "score": round(confidence, 3),
        "match_type": match_type,
        "components": {
            "name": round(name_score, 2),
            "description": round(desc_score, 2),
            "activity": round(activity_score, 2),
            "penalty": round(penalty, 2)
        }
    }


def discover_subreddits(
    query: Optional[str] = None,
    queries: Optional[Union[List[str], str]] = None,
    reddit: praw.Reddit = None,
    limit: int = 10,
    include_nsfw: bool = False
) -> Dict[str, Any]:
    """
    Search for subreddits by keyword or topic. Supports batch queries.
    
    Args:
        query: Single search term to find subreddits
        queries: List of search terms for batch discovery (more efficient) 
                 Can also be a JSON string like '["term1", "term2"]'
        reddit: Reddit instance
        limit: Maximum number of results per query (default 10)
        include_nsfw: Whether to include NSFW subreddits (default False)
    
    Returns:
        Dictionary with discovered subreddits and their metadata
    """
    # Handle batch queries - convert string to list if needed
    if queries:
        # Handle case where LLM passes JSON string instead of array
        if isinstance(queries, str):
            try:
                # Try to parse as JSON if it looks like a JSON array
                if queries.strip().startswith('[') and queries.strip().endswith(']'):
                    queries = json.loads(queries)
                else:
                    # Single string query, convert to single-item list
                    queries = [queries]
            except (json.JSONDecodeError, ValueError):
                # If JSON parsing fails, treat as single string
                queries = [queries]
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
            "results": [],
            "summary": {
                "total_found": 0,
                "returned": 0,
                "coverage": "error"
            }
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
        # Fetch more results for comprehensive coverage
        fetch_limit = 250  # Get broader results for better discovery
        
        for subreddit in reddit.subreddits.search(query, limit=fetch_limit):
            total_found += 1
            
            # Skip NSFW subreddits if not requested
            if subreddit.over18 and not include_nsfw:
                nsfw_filtered += 1
                continue
                
            try:
                # Validate subreddit exists and is accessible
                _ = subreddit.id  # This will fail if subreddit doesn't exist
                
                # Calculate confidence score
                confidence_data = calculate_confidence(subreddit, query)
                
                results.append({
                    "name": subreddit.display_name,
                    "title": subreddit.title,
                    "description": subreddit.public_description[:100] if subreddit.public_description else "No description",
                    "subscribers": subreddit.subscribers,
                    "over_18": subreddit.over18,
                    "url": f"https://reddit.com/r/{subreddit.display_name}",
                    "created_utc": subreddit.created_utc,
                    "confidence": confidence_data["score"],
                    "match_type": confidence_data["match_type"],
                    "score_breakdown": confidence_data["components"]
                })
                    
            except Exception:
                # Skip inaccessible subreddits
                continue
        
        # Sort results by confidence score (highest first), then by subscribers
        results.sort(key=lambda x: (-x['confidence'], -(x['subscribers'] or 0)))
        
        # Limit to requested number
        limited_results = results[:limit]
        
        # Determine coverage quality
        if total_found >= 200:
            coverage = "comprehensive"
        elif total_found >= 50:
            coverage = "good"
        elif total_found >= 10:
            coverage = "partial"
        else:
            coverage = "limited"
        
        # Get top high-confidence subreddits for quick reference
        high_confidence_results = [r for r in limited_results if r['confidence'] >= 0.5]
        top_by_confidence = [r['name'] for r in high_confidence_results[:5]]
        
        # Calculate confidence distribution
        confidence_dist = {
            "high": len([r for r in limited_results if r['confidence'] >= 0.7]),
            "medium": len([r for r in limited_results if 0.4 <= r['confidence'] < 0.7]),
            "low": len([r for r in limited_results if r['confidence'] < 0.4])
        }
        
        # Generate next actions for LLM
        next_actions = ["Use exact 'name' field when calling other tools"]
        if len(results) > limit:
            next_actions.append(f"More results available - found {len(results)} total, returned {limit}")
        if nsfw_filtered > 0:
            next_actions.append(f"{nsfw_filtered} NSFW subreddits filtered - set include_nsfw=True to see them")
        if confidence_dist["low"] > confidence_dist["high"]:
            next_actions.append("Consider refining search query for better matches")
        
        # Generate search suggestions if few results
        search_suggestions = []
        if total_found < 10:
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
            "results": limited_results,
            "summary": {
                "total_found": total_found,
                "returned": len(limited_results),
                "coverage": coverage,
                "top_by_confidence": top_by_confidence,
                "confidence_distribution": confidence_dist,
                "nsfw_filtered": nsfw_filtered
            },
            "next_actions": next_actions
        }
        
        # Only add suggestions if there are any
        if search_suggestions:
            response["search_suggestions"] = search_suggestions
        
        return response
        
    except Exception as e:
        return {
            "error": f"Failed to search for subreddits: {str(e)}",
            "query": query,
            "results": [],
            "summary": {
                "total_found": 0,
                "returned": 0,
                "coverage": "error",
                "top_by_confidence": [],
                "confidence_distribution": {"high": 0, "medium": 0, "low": 0},
                "nsfw_filtered": 0
            },
            "next_actions": ["Check error message and retry"]
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