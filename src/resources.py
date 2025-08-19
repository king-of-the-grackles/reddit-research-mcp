"""Reddit MCP Resources - Static and cacheable data endpoints."""

from typing import Dict, List, Any
import praw


def register_resources(mcp, reddit: praw.Reddit) -> None:
    """Register all Reddit resources with the MCP server."""
    
    @mcp.resource("reddit://popular-subreddits")
    def get_popular_subreddits() -> Dict[str, Any]:
        """
        Get list of 25 most popular subreddits.
        
        Returns a list of popular subreddits with their subscriber counts.
        This data is relatively static and ideal for caching.
        """
        try:
            subreddits = []
            for subreddit in reddit.subreddits.popular(limit=25):
                subreddits.append({
                    "name": subreddit.display_name,
                    "title": subreddit.title,
                    "subscribers": subreddit.subscribers,
                    "description": subreddit.public_description[:200] if subreddit.public_description else "",
                    "url": f"https://reddit.com/r/{subreddit.display_name}"
                })
            
            return {
                "count": len(subreddits),
                "subreddits": subreddits
            }
        except Exception as e:
            return {
                "error": f"Failed to fetch popular subreddits: {str(e)}",
                "subreddits": []
            }
    
    @mcp.resource("reddit://subreddit/{name}/about")
    def get_subreddit_about(name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific subreddit.
        
        Args:
            name: The subreddit name (without r/ prefix)
            
        Returns information including description, rules, and statistics.
        """
        try:
            subreddit = reddit.subreddit(name)
            
            # Fetch basic info
            info = {
                "name": subreddit.display_name,
                "title": subreddit.title,
                "description": subreddit.public_description,
                "subscribers": subreddit.subscribers,
                "active_users": subreddit.active_user_count,
                "created_utc": subreddit.created_utc,
                "over_18": subreddit.over18,
                "url": f"https://reddit.com/r/{subreddit.display_name}"
            }
            
            # Try to fetch rules
            try:
                rules = []
                for rule in subreddit.rules:
                    rules.append({
                        "short_name": rule.short_name,
                        "description": rule.description,
                        "violation_reason": rule.violation_reason
                    })
                info["rules"] = rules
            except:
                info["rules"] = []
            
            return info
            
        except praw.exceptions.RedditAPIException as e:
            return {
                "error": f"Subreddit '{name}' not found or inaccessible",
                "details": str(e)
            }
        except Exception as e:
            return {
                "error": f"Failed to fetch subreddit info: {str(e)}"
            }
    
    @mcp.resource("reddit://server-info")
    def get_server_info() -> Dict[str, Any]:
        """
        Get information about this Reddit MCP server's capabilities.
        
        Returns server version, available tools, and usage examples.
        """
        # Try to get rate limit info from Reddit
        rate_limit_info = {}
        try:
            # Access auth to check rate limit status
            rate_limit_info = {
                "requests_remaining": reddit.auth.limits.get('remaining', 'unknown'),
                "reset_timestamp": reddit.auth.limits.get('reset_timestamp', 'unknown'),
                "used": reddit.auth.limits.get('used', 'unknown')
            }
        except:
            rate_limit_info = {
                "status": "Rate limits tracked automatically by PRAW",
                "strategy": "Automatic retry with exponential backoff"
            }
        
        return {
            "name": "Reddit MCP Server",
            "version": "0.3.0",
            "description": "A Model Context Protocol server for Reddit using three-layer architecture",
            "changelog": {
                "0.3.0": [
                    "Implemented three-layer architecture for clearer operation flow",
                    "Removed search_all operation in favor of semantic discovery",
                    "Enhanced workflow guidance with confidence-based recommendations",
                    "Improved error recovery suggestions"
                ],
                "0.2.0": [
                    "Added discover_subreddits with confidence scoring",
                    "Added fetch_multiple_subreddits for batch operations",
                    "Enhanced server-info with comprehensive documentation",
                    "Improved error handling and rate limit management"
                ],
                "0.1.0": [
                    "Initial release with search, fetch, and comment tools",
                    "Basic resources for popular subreddits and server info"
                ]
            },
            "capabilities": {
                "architecture": {
                    "type": "Three-Layer Architecture",
                    "workflow": [
                        "Layer 1: discover_operations() - See available operations",
                        "Layer 2: get_operation_schema(operation_id) - Get requirements",
                        "Layer 3: execute_operation(operation_id, parameters) - Execute"
                    ],
                    "description": "ALWAYS start with Layer 1, then Layer 2, then Layer 3"
                },
                "tools": [
                    {
                        "name": "discover_operations",
                        "layer": 1,
                        "description": "Discover available Reddit operations",
                        "parameters": "None - just call discover_operations() to see what's available",
                        "purpose": "Shows all available operations and recommended workflows"
                    },
                    {
                        "name": "get_operation_schema",
                        "layer": 2,
                        "description": "Get parameter requirements for an operation",
                        "parameters": {
                            "operation_id": "The operation to get schema for (from Layer 1)",
                            "include_examples": "Whether to include examples (optional, default: true)"
                        },
                        "purpose": "Provides parameter schemas, validation rules, and examples"
                    },
                    {
                        "name": "execute_operation",
                        "layer": 3,
                        "description": "Execute a Reddit operation",
                        "parameters": {
                            "operation_id": "The operation to execute",
                            "parameters": "Parameters matching the schema from Layer 2"
                        },
                        "purpose": "Actually performs the Reddit API calls"
                    }
                ],
                "available_operations": {
                    "discover_subreddits": "Find communities using semantic search",
                    "search_subreddit": "Search within a specific community",
                    "fetch_posts": "Get posts from one subreddit",
                    "fetch_multiple": "Batch fetch from multiple subreddits (70% more efficient)",
                    "fetch_comments": "Get complete comment tree for analysis"
                },
                "resources": [
                    {
                        "uri": "reddit://popular-subreddits",
                        "description": "List of 25 most popular subreddits",
                        "cacheable": True,
                        "refresh_interval": "24 hours recommended"
                    },
                    {
                        "uri": "reddit://subreddit/{name}/about",
                        "description": "Detailed information about a specific subreddit including rules",
                        "cacheable": True,
                        "refresh_interval": "1 hour recommended"
                    },
                    {
                        "uri": "reddit://server-info",
                        "description": "Server capabilities, version, and usage information",
                        "cacheable": False,
                        "always_current": True
                    }
                ],
                "total_tools": 3,
                "total_operations": 5,
                "total_resources": 3
            },
            "usage_examples": {
                "complete_workflow": [
                    "Step 1: discover_operations()",
                    "Step 2: get_operation_schema('discover_subreddits')",
                    "Step 3: execute_operation('discover_subreddits', {'query': 'python', 'limit': 10})"
                ],
                "research_workflow": [
                    "1. discover_operations() - See what's available",
                    "2. get_operation_schema('discover_subreddits') - Get requirements",
                    "3. execute_operation('discover_subreddits', {'query': 'texas redistricting'})",
                    "4. get_operation_schema('fetch_multiple') - Get batch fetch requirements",
                    "5. execute_operation('fetch_multiple', {'subreddit_names': ['texas', 'politics']})",
                    "6. get_operation_schema('fetch_comments') - Get comment fetch requirements",
                    "7. execute_operation('fetch_comments', {'submission_id': '1abc234'})"
                ],
                "targeted_search": [
                    "1. discover_operations()",
                    "2. get_operation_schema('discover_subreddits')",
                    "3. execute_operation('discover_subreddits', {'query': 'machine learning'})",
                    "4. get_operation_schema('search_subreddit')",
                    "5. execute_operation('search_subreddit', {'subreddit_name': 'MachineLearning', 'query': 'transformers'})"
                ]
            },
            "performance_tips": [
                "Always follow the three-layer workflow: discover → schema → execute",
                "Use fetch_multiple operation for 2+ subreddits (70% fewer API calls)",
                "Single vector search in discover_subreddits finds all relevant communities",
                "Use confidence scores to determine workflow (>0.7 = high confidence)",
                "Cache resource responses when appropriate (popular-subreddits, subreddit/about)"
            ],
            "workflow_guidance": {
                "starting_research": {
                    "description": "For any new topic, always start with the three layers",
                    "steps": [
                        "1. discover_operations() - No parameters needed",
                        "2. get_operation_schema('discover_subreddits')",
                        "3. execute_operation('discover_subreddits', {'query': 'your_topic'})"
                    ]
                },
                "confidence_based_workflow": {
                    "high_confidence": "If avg confidence > 0.7: Use fetch_multiple with top communities",
                    "medium_confidence": "If avg confidence 0.4-0.7: Combine fetch_multiple and search_subreddit",
                    "low_confidence": "If avg confidence < 0.4: Try different search terms"
                },
                "token_optimization": {
                    "discover_subreddits": "Single semantic search (~1-2K tokens)",
                    "fetch_multiple": "Batch fetch (~500-1000 tokens per subreddit)",
                    "fetch_comments": "Deep analysis (~2-5K tokens per post with comments)"
                }
            },
            "rate_limiting": {
                "handler": "PRAW automatic rate limit handling",
                "strategy": "Exponential backoff with 5-minute cooldown",
                "current_status": rate_limit_info
            },
            "authentication": {
                "type": "Application-only OAuth",
                "scope": "Read-only access",
                "capabilities": "Search, browse, and read public content"
            },
            "api_efficiency": {
                "batch_operations": [
                    "discover_subreddits_tool supports batch queries",
                    "fetch_multiple_subreddits_tool fetches from multiple subreddits at once"
                ],
                "caching_recommendations": [
                    "Cache popular-subreddits for 24 hours",
                    "Cache subreddit/about for 1 hour",
                    "Search results can be cached for 5-15 minutes depending on sort type"
                ]
            }
        }