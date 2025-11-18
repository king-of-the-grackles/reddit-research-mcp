"""Reddit MCP Tools - Semantic discovery and Reddit research operations.

Export key classes and functions for public API.
"""

from .discover import (
    discover_subreddits,
    validate_subreddit,
    SearchConfig,
    DEFAULT_SEARCH_CONFIG,
    calculate_confidence_from_distance,
    classify_match_tier,
)

from .watchlist import (
    create_watchlist,
    list_watchlists,
    get_watchlist,
    update_watchlist,
    delete_watchlist,
)

__all__ = [
    # Reddit discovery
    "discover_subreddits",
    "validate_subreddit",
    "SearchConfig",
    "DEFAULT_SEARCH_CONFIG",
    "calculate_confidence_from_distance",
    "classify_match_tier",
    # Watchlists
    "create_watchlist",
    "list_watchlists",
    "get_watchlist",
    "update_watchlist",
    "delete_watchlist",
]
