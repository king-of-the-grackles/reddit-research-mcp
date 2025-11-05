"""Subreddit discovery using semantic vector search."""

import os
import json
from typing import Dict, List, Optional, Union, Any
from fastmcp import Context
from ..chroma_client import get_chroma_client, get_collection


def classify_match_tier(distance: float) -> str:
    """
    Classify semantic match quality based on distance.

    Distance scale (Euclidean):
    - 0.0-0.2: exact (highly relevant)
    - 0.2-0.35: semantic (very relevant)
    - 0.35-0.65: adjacent (somewhat relevant)
    - 0.65+: peripheral (weakly relevant)

    Args:
        distance: Euclidean distance from query embedding

    Returns:
        Match tier label: "exact", "semantic", "adjacent", or "peripheral"
    """
    if distance < 0.2:
        return "exact"
    elif distance < 0.35:
        return "semantic"
    elif distance < 0.65:
        return "adjacent"
    else:
        return "peripheral"


def calculate_confidence_stats(confidence_scores: List[float]) -> Dict[str, float]:
    """
    Calculate statistics about confidence score distribution.

    Args:
        confidence_scores: List of confidence scores (0.0-1.0)

    Returns:
        Dictionary with mean, median, min, max, and standard deviation
    """
    if not confidence_scores:
        return {
            "mean": 0.0,
            "median": 0.0,
            "min": 0.0,
            "max": 0.0,
            "std_dev": 0.0
        }

    import statistics

    sorted_scores = sorted(confidence_scores)
    return {
        "mean": round(statistics.mean(confidence_scores), 3),
        "median": round(sorted_scores[len(sorted_scores) // 2], 3),
        "min": round(min(confidence_scores), 3),
        "max": round(max(confidence_scores), 3),
        "std_dev": round(statistics.stdev(confidence_scores), 3) if len(confidence_scores) > 1 else 0.0
    }


def calculate_tier_distribution(results: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Count results by match tier.

    Args:
        results: List of result dictionaries with 'match_tier' field

    Returns:
        Dictionary with counts for each tier
    """
    tier_counts = {"exact": 0, "semantic": 0, "adjacent": 0, "peripheral": 0}

    for result in results:
        tier = result.get('match_tier', 'peripheral')
        if tier in tier_counts:
            tier_counts[tier] += 1

    return tier_counts


async def discover_subreddits(
    query: Optional[str] = None,
    queries: Optional[Union[List[str], str]] = None,
    limit: int = 10,
    include_nsfw: bool = False,
    min_confidence: float = 0.0,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Search for subreddits using semantic similarity search.

    Finds relevant subreddits based on semantic embeddings of subreddit names,
    descriptions, and community metadata.

    Args:
        query: Single search term to find subreddits
        queries: List of search terms for batch discovery (more efficient)
                 Can also be a JSON string like '["term1", "term2"]'
        limit: Maximum number of results per query (default 10)
        include_nsfw: Whether to include NSFW subreddits (default False)
        min_confidence: Minimum confidence score to include (0.0-1.0, default 0.0)
        ctx: FastMCP context (auto-injected by decorator)

    Returns:
        Dictionary with discovered subreddits and their metadata
    """
    # Phase 1: Accept context but don't use it yet

    # Initialize ChromaDB client
    try:
        client = get_chroma_client()
        collection = get_collection("reddit_subreddits", client)
        
    except Exception as e:
        return {
            "error": f"Failed to connect to vector database: {str(e)}",
            "results": [],
            "summary": {
                "total_found": 0,
                "returned": 0,
                "coverage": "error"
            }
        }
    
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
            result = await _search_vector_db(
                search_query, collection, limit, include_nsfw, min_confidence, ctx
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
        return await _search_vector_db(query, collection, limit, include_nsfw, min_confidence, ctx)
    
    else:
        return {
            "error": "Either 'query' or 'queries' parameter must be provided",
            "subreddits": [],
            "summary": {
                "total_found": 0,
                "returned": 0,
                "coverage": "error"
            }
        }


async def _search_vector_db(
    query: str,
    collection,
    limit: int,
    include_nsfw: bool,
    min_confidence: float,
    ctx: Context = None
) -> Dict[str, Any]:
    """Internal function to perform semantic search for a single query."""
    # Phase 1: Accept context but don't use it yet

    try:
        # Search with a larger limit to allow for filtering
        search_limit = min(limit * 3, 100)  # Get extra results for filtering
        
        # Perform semantic search
        results = collection.query(
            query_texts=[query],
            n_results=search_limit
        )
        
        if not results or not results['metadatas'] or not results['metadatas'][0]:
            return {
                "query": query,
                "subreddits": [],
                "summary": {
                    "total_found": 0,
                    "returned": 0,
                    "has_more": False
                },
                "next_actions": ["Try different search terms"]
            }
        
        # Process results
        processed_results = []
        nsfw_filtered = 0
        total_results = len(results['metadatas'][0])

        for i, (metadata, distance) in enumerate(zip(
            results['metadatas'][0],
            results['distances'][0]
        )):
            # Report progress
            if ctx:
                await ctx.report_progress(
                    progress=i + 1,
                    total=total_results,
                    message=f"Analyzing r/{metadata.get('name', 'unknown')}"
                )

            # Skip NSFW if not requested
            if metadata.get('nsfw', False) and not include_nsfw:
                nsfw_filtered += 1
                continue
            
            # Convert distance to confidence score (lower distance = higher confidence)
            # Adjust the scaling based on observed distances (typically 0.8 to 1.6)
            # Map distances: 0.8 -> 0.9, 1.0 -> 0.7, 1.2 -> 0.5, 1.4 -> 0.3, 1.6+ -> 0.1
            if distance < 0.8:
                confidence = 0.9 + (0.1 * (0.8 - distance) / 0.8)  # 0.9 to 1.0
            elif distance < 1.0:
                confidence = 0.7 + (0.2 * (1.0 - distance) / 0.2)  # 0.7 to 0.9
            elif distance < 1.2:
                confidence = 0.5 + (0.2 * (1.2 - distance) / 0.2)  # 0.5 to 0.7
            elif distance < 1.4:
                confidence = 0.3 + (0.2 * (1.4 - distance) / 0.2)  # 0.3 to 0.5
            else:
                confidence = max(0.1, 0.3 * (2.0 - distance) / 0.6)  # 0.1 to 0.3
            
            # Apply penalties for generic subreddits
            subreddit_name = metadata.get('name', '').lower()
            generic_subs = ['funny', 'pics', 'videos', 'gifs', 'memes', 'aww']
            if subreddit_name in generic_subs and query.lower() not in subreddit_name:
                confidence *= 0.3  # Heavy penalty for generic subs unless directly searched
            
            # Boost for high-activity subreddits (optional)
            subscribers = metadata.get('subscribers', 0)
            if subscribers > 1000000:
                confidence = min(1.0, confidence * 1.1)  # Small boost for very large subs
            elif subscribers < 10000:
                confidence *= 0.9  # Small penalty for tiny subs
            
            # Determine match type based on distance
            if distance < 0.3:
                match_type = "exact_match"
            elif distance < 0.7:
                match_type = "strong_match"
            elif distance < 1.0:
                match_type = "partial_match"
            else:
                match_type = "weak_match"

            # Classify match tier for Phase 2a.2
            match_tier = classify_match_tier(distance)

            processed_results.append({
                "name": metadata.get('name', 'unknown'),
                "subscribers": metadata.get('subscribers', 0),
                "confidence": round(confidence, 3),
                "distance": round(distance, 3),
                "match_tier": match_tier,
                "url": metadata.get('url', f"https://reddit.com/r/{metadata.get('name', '')}")
            })

        # Filter by minimum confidence if specified (Phase 2a.3)
        if min_confidence > 0.0:
            processed_results = [
                r for r in processed_results
                if r['confidence'] >= min_confidence
            ]

        # Sort by confidence (highest first), then by subscribers
        processed_results.sort(key=lambda x: (-x['confidence'], -(x['subscribers'] or 0)))
        
        # Limit to requested number
        limited_results = processed_results[:limit]
        
        # Calculate basic stats
        total_found = len(processed_results)

        # Calculate confidence statistics (Phase 2a.4)
        confidence_scores = [r['confidence'] for r in limited_results]
        confidence_stats = calculate_confidence_stats(confidence_scores)
        tier_distribution = calculate_tier_distribution(limited_results)

        # Generate next actions (only meaningful ones)
        next_actions = []
        if len(processed_results) > limit:
            next_actions.append(f"{len(processed_results)} total results found, showing {limit}")
        if nsfw_filtered > 0:
            next_actions.append(f"{nsfw_filtered} NSFW subreddits filtered")

        return {
            "query": query,
            "subreddits": limited_results,
            "summary": {
                "total_found": total_found,
                "returned": len(limited_results),
                "has_more": total_found > len(limited_results),
                "confidence_stats": confidence_stats,
                "tier_distribution": tier_distribution
            },
            "next_actions": next_actions
        }
        
    except Exception as e:
        # Map error patterns to specific recovery actions
        error_str = str(e).lower()
        if "not found" in error_str:
            guidance = "Verify subreddit name spelling"
        elif "rate" in error_str:
            guidance = "Rate limited - wait 60 seconds"
        elif "timeout" in error_str:
            guidance = "Reduce limit parameter to 10"
        else:
            guidance = "Try simpler search terms"
            
        return {
            "error": f"Failed to search vector database: {str(e)}",
            "query": query,
            "subreddits": [],
            "summary": {
                "total_found": 0,
                "returned": 0,
                "has_more": False
            },
            "next_actions": [guidance]
        }


def validate_subreddit(
    subreddit_name: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Validate if a subreddit exists in the indexed database.

    Checks if the subreddit exists in our semantic search index
    and returns its metadata if found.

    Args:
        subreddit_name: Name of the subreddit to validate
        ctx: FastMCP context (optional)

    Returns:
        Dictionary with validation result and subreddit info if found
    """
    # Phase 1: Accept context but don't use it yet

    # Clean the subreddit name
    clean_name = subreddit_name.replace("r/", "").replace("/r/", "").strip()
    
    try:
        # Search for exact match in vector database
        client = get_chroma_client()
        collection = get_collection("reddit_subreddits", client)
        
        # Search for the exact subreddit name
        results = collection.query(
            query_texts=[clean_name],
            n_results=5
        )
        
        if results and results['metadatas'] and results['metadatas'][0]:
            # Look for exact match in results
            for metadata in results['metadatas'][0]:
                if metadata.get('name', '').lower() == clean_name.lower():
                    return {
                        "valid": True,
                        "name": metadata.get('name'),
                        "subscribers": metadata.get('subscribers', 0),
                        "is_private": False,  # We only index public subreddits
                        "over_18": metadata.get('nsfw', False),
                        "indexed": True
                    }
        
        return {
            "valid": False,
            "name": clean_name,
            "error": f"Subreddit '{clean_name}' not found",
            "suggestion": "Use discover_subreddits to find similar communities"
        }
        
    except Exception as e:
        return {
            "valid": False,
            "name": clean_name,
            "error": f"Database error: {str(e)}",
            "suggestion": "Check database connection and retry"
        }