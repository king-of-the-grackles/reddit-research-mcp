"""Subreddit discovery using semantic vector search."""

import os
import json
import statistics
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from fastmcp import Context
from ..chroma_client import get_chroma_client, get_collection


@dataclass
class SearchConfig:
    """Centralized configuration for semantic search behavior.

    All parameters are tunable to adjust search sensitivity and result filtering.
    """

    # Distance-to-tier thresholds (Euclidean distance)
    EXACT_DISTANCE_THRESHOLD: float = 0.2      # Very relevant matches
    SEMANTIC_DISTANCE_THRESHOLD: float = 0.35  # Relevant matches
    ADJACENT_DISTANCE_THRESHOLD: float = 0.65  # Somewhat relevant

    # Confidence score mapping (maps distance ranges to confidence 0.0-1.0)
    # Lower distance = higher confidence
    CONFIDENCE_DISTANCE_BREAKPOINTS: Dict[float, float] = None

    # Generic subreddit filtering
    GENERIC_SUBREDDITS: List[str] = None
    GENERIC_PENALTY_MULTIPLIER: float = 0.3    # Penalty when generic sub matches broadly

    # Subscriber-based scoring
    LARGE_SUB_THRESHOLD: int = 1_000_000       # Boost applied above this
    LARGE_SUB_BOOST_MULTIPLIER: float = 1.1    # Boost factor for large subs
    SMALL_SUB_THRESHOLD: int = 10_000          # Penalty applied below this
    SMALL_SUB_PENALTY_MULTIPLIER: float = 0.9  # Penalty factor for small subs

    # Search behavior
    SEARCH_MULTIPLIER: int = 3                 # Fetch 3x limit for filtering
    MAX_SEARCH_RESULTS: int = 100              # Hard cap on returned results

    def __post_init__(self):
        """Initialize default values for mutable fields."""
        if self.GENERIC_SUBREDDITS is None:
            self.GENERIC_SUBREDDITS = [
                'funny', 'pics', 'videos', 'gifs', 'memes', 'aww', 'news', 'science'
            ]
        if self.CONFIDENCE_DISTANCE_BREAKPOINTS is None:
            # Maps distance thresholds to confidence ranges
            # Distance range -> confidence range
            self.CONFIDENCE_DISTANCE_BREAKPOINTS = {
                0.8: 0.95,      # <0.8:  0.9-1.0
                1.0: 0.80,      # 0.8-1.0: 0.7-0.9
                1.2: 0.60,      # 1.0-1.2: 0.5-0.7
                1.4: 0.40,      # 1.2-1.4: 0.3-0.5
                2.0: 0.15       # 1.4-2.0: 0.1-0.3
            }


# Global default configuration
DEFAULT_SEARCH_CONFIG = SearchConfig()


def classify_match_tier(distance: float, config: SearchConfig = None) -> str:
    """
    Classify semantic match quality based on distance.

    Uses configurable thresholds to categorize match relevance.
    Distance scale (Euclidean, lower is better):
    - 0.0-0.2: exact (highly relevant)
    - 0.2-0.35: semantic (very relevant)
    - 0.35-0.65: adjacent (somewhat relevant)
    - 0.65+: peripheral (weakly relevant)

    Args:
        distance: Euclidean distance from query embedding
        config: SearchConfig instance with tunable thresholds

    Returns:
        Match tier label: "exact", "semantic", "adjacent", or "peripheral"
    """
    if config is None:
        config = DEFAULT_SEARCH_CONFIG

    if distance < config.EXACT_DISTANCE_THRESHOLD:
        return "exact"
    elif distance < config.SEMANTIC_DISTANCE_THRESHOLD:
        return "semantic"
    elif distance < config.ADJACENT_DISTANCE_THRESHOLD:
        return "adjacent"
    else:
        return "peripheral"


def calculate_confidence_stats(confidence_scores: List[float]) -> Dict[str, float]:
    """
    Calculate statistics about confidence score distribution.

    Provides insight into the quality and variance of matched results.

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

    sorted_scores = sorted(confidence_scores)
    return {
        "mean": round(statistics.mean(confidence_scores), 3),
        "median": round(sorted_scores[len(sorted_scores) // 2], 3),
        "min": round(min(confidence_scores), 3),
        "max": round(max(confidence_scores), 3),
        "std_dev": round(statistics.stdev(confidence_scores), 3) if len(confidence_scores) > 1 else 0.0
    }


def _get_vector_collection(collection_name: str = "dialog-app-prod-db"):
    """
    Initialize ChromaDB client and retrieve a collection.

    Helper function to reduce code duplication across discovery operations.

    Args:
        collection_name: Name of the ChromaDB collection to retrieve

    Returns:
        ChromaDB collection object

    Raises:
        Exception: If connection or collection retrieval fails
    """
    client = get_chroma_client()
    return get_collection(collection_name, client)


def calculate_confidence_from_distance(distance: float, config: SearchConfig = None) -> float:
    """
    Convert Euclidean distance to confidence score (0.0-1.0).

    Uses a piecewise linear interpolation model mapping distance ranges to
    confidence bands. Lower distance = higher confidence.

    Distance ranges map as follows:
    - <0.8:   confidence 0.90-1.0   (excellent match)
    - 0.8-1.0: confidence 0.70-0.9  (strong match)
    - 1.0-1.2: confidence 0.50-0.7  (moderate match)
    - 1.2-1.4: confidence 0.30-0.5  (weak match)
    - 1.4-2.0: confidence 0.10-0.3  (very weak match)

    Args:
        distance: Euclidean distance from query embedding
        config: SearchConfig with confidence mapping parameters

    Returns:
        Confidence score between 0.0 and 1.0

    Example:
        >>> calculate_confidence_from_distance(0.5)
        0.937  # Very high confidence for close match
        >>> calculate_confidence_from_distance(1.2)
        0.6    # Moderate confidence
    """
    if config is None:
        config = DEFAULT_SEARCH_CONFIG

    breakpoints = sorted(config.CONFIDENCE_DISTANCE_BREAKPOINTS.items())

    # Find which bracket the distance falls into
    for i, (threshold, confidence_at_threshold) in enumerate(breakpoints):
        if distance <= threshold:
            if i == 0:
                # Before first breakpoint: linearly interpolate from 1.0 to confidence_at_threshold
                prior_threshold = 0.0
                prior_confidence = 1.0
            else:
                prior_threshold, prior_confidence = breakpoints[i - 1]

            # Linear interpolation between prior and current threshold
            if threshold == prior_threshold:
                return confidence_at_threshold
            interpolation = (distance - prior_threshold) / (threshold - prior_threshold)
            confidence = prior_confidence - (prior_confidence - confidence_at_threshold) * interpolation
            return round(max(0.0, min(1.0, confidence)), 3)

    # Beyond last breakpoint, return minimum confidence
    return 0.1


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
    config: Optional[SearchConfig] = None,
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
        config: SearchConfig instance for tuning behavior (uses defaults if None)
        ctx: FastMCP context (auto-injected by decorator)

    Returns:
        Dictionary with discovered subreddits and their metadata
    """
    if config is None:
        config = DEFAULT_SEARCH_CONFIG

    # Initialize ChromaDB client
    try:
        collection = _get_vector_collection("dialog-app-prod-db")

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
                search_query, collection, limit, include_nsfw, min_confidence, config, ctx
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
        return await _search_vector_db(query, collection, limit, include_nsfw, min_confidence, config, ctx)
    
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
    config: SearchConfig = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Internal function to perform semantic search for a single query.

    Args:
        query: Search query string
        collection: ChromaDB collection object
        limit: Max results to return
        include_nsfw: Whether to include NSFW subreddits
        min_confidence: Minimum confidence threshold
        config: SearchConfig with tunable parameters
        ctx: FastMCP context for progress reporting

    Returns:
        Dictionary with search results and statistics
    """
    if config is None:
        config = DEFAULT_SEARCH_CONFIG

    try:
        # Search with a larger limit to allow for filtering
        search_limit = min(limit * config.SEARCH_MULTIPLIER, config.MAX_SEARCH_RESULTS)
        
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
            
            # Convert distance to confidence score using configurable model
            confidence = calculate_confidence_from_distance(distance, config)

            # Apply penalties for generic subreddits (configurable)
            subreddit_name = metadata.get('name', '').lower()
            if subreddit_name in config.GENERIC_SUBREDDITS and query.lower() not in subreddit_name:
                confidence *= config.GENERIC_PENALTY_MULTIPLIER

            # Apply boosts/penalties based on subscriber count
            subscribers = metadata.get('subscribers', 0)
            if subscribers > config.LARGE_SUB_THRESHOLD:
                confidence = min(1.0, confidence * config.LARGE_SUB_BOOST_MULTIPLIER)
            elif subscribers < config.SMALL_SUB_THRESHOLD:
                confidence *= config.SMALL_SUB_PENALTY_MULTIPLIER
            
            # Determine match type based on distance
            if distance < 0.3:
                match_type = "exact_match"
            elif distance < 0.7:
                match_type = "strong_match"
            elif distance < 1.0:
                match_type = "partial_match"
            else:
                match_type = "weak_match"

            # Classify match tier based on distance
            match_tier = classify_match_tier(distance, config)

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
    # Clean the subreddit name
    clean_name = subreddit_name.replace("r/", "").replace("/r/", "").strip()

    try:
        # Search for exact match in vector database
        collection = _get_vector_collection("dialog-app-prod-db")
        
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