from fastmcp import FastMCP
from typing import Optional, Literal, List, Union, Dict, Any, Annotated
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_reddit_client
from src.tools.search import search_in_subreddit
from src.tools.posts import fetch_subreddit_posts, fetch_multiple_subreddits
from src.tools.comments import fetch_submission_with_comments
from src.tools.discover import discover_subreddits
from src.resources import register_resources

# Initialize MCP server
mcp = FastMCP("Reddit MCP", instructions="""
Reddit MCP Server - Three-Layer Architecture

🎯 ALWAYS FOLLOW THIS WORKFLOW:
1. discover_operations() - See what's available
2. get_operation_schema() - Understand requirements  
3. execute_operation() - Perform the action

📊 RESEARCH BEST PRACTICES:
• Start with discover_subreddits for ANY topic
• Use confidence scores to guide workflow:
  - High (>0.7): Direct to specific communities
  - Medium (0.4-0.7): Multi-community approach
  - Low (<0.4): Refine search terms
• Fetch comments for 10+ posts for thorough analysis
• Always include Reddit URLs when citing content

⚡ EFFICIENCY TIPS:
• Use fetch_multiple for 2+ subreddits (70% fewer API calls)
• Single vector search finds semantically related communities
• Batch operations reduce token usage

Quick Start: Read reddit://server-info for complete documentation.
""")

# Initialize Reddit client
reddit = get_reddit_client()

# Register resources
register_resources(mcp, reddit)


# Three-Layer Architecture Implementation

@mcp.tool(
    description="Discover available Reddit operations and recommended workflows",
    annotations={"readOnlyHint": True}
)
def discover_operations() -> Dict[str, Any]:
    """
    LAYER 1: Discover what operations this MCP server provides.
    Start here to understand available capabilities.
    """
    return {
        "operations": {
            "discover_subreddits": "Find relevant communities using semantic search",
            "search_subreddit": "Search for posts within a specific community",
            "fetch_posts": "Get posts from a single subreddit",
            "fetch_multiple": "Batch fetch from multiple subreddits (70% more efficient)",
            "fetch_comments": "Get complete comment tree for deep analysis"
        },
        "recommended_workflows": {
            "comprehensive_research": [
                "discover_subreddits → fetch_multiple → fetch_comments",
                "Best for: Thorough analysis across communities"
            ],
            "targeted_search": [
                "discover_subreddits → search_subreddit → fetch_comments",
                "Best for: Finding specific content in relevant communities"
            ]
        },
        "next_step": "Use get_operation_schema() to understand requirements"
    }


@mcp.tool(
    description="Get detailed requirements and parameters for a Reddit operation",
    annotations={"readOnlyHint": True}
)
def get_operation_schema(
    operation_id: Annotated[str, "Operation ID from discover_operations"],
    include_examples: Annotated[bool, "Include example parameter values"] = True
) -> Dict[str, Any]:
    """
    LAYER 2: Get parameter requirements for an operation.
    Use after discover_operations to understand how to call operations.
    """
    schemas = {
        "discover_subreddits": {
            "description": "Find communities using semantic vector search",
            "parameters": {
                "query": {
                    "type": "string",
                    "required": True,
                    "description": "Topic to find communities for",
                    "validation": "2-100 characters"
                },
                "limit": {
                    "type": "integer",
                    "required": False,
                    "default": 10,
                    "range": [1, 50],
                    "description": "Number of communities to return"
                },
                "include_nsfw": {
                    "type": "boolean",
                    "required": False,
                    "default": False,
                    "description": "Whether to include NSFW communities"
                }
            },
            "returns": {
                "subreddits": "Array with confidence scores (0-1)",
                "quality_indicators": {
                    "good": "5+ subreddits with confidence > 0.7",
                    "poor": "All results below 0.5 confidence"
                }
            },
            "examples": [] if not include_examples else [
                {"query": "machine learning", "limit": 15},
                {"query": "python web development", "limit": 10}
            ]
        },
        "search_subreddit": {
            "description": "Search for posts within a specific subreddit",
            "parameters": {
                "subreddit_name": {
                    "type": "string",
                    "required": True,
                    "description": "Exact subreddit name (without r/ prefix)",
                    "tip": "Use exact name from discover_subreddits"
                },
                "query": {
                    "type": "string",
                    "required": True,
                    "description": "Search terms"
                },
                "sort": {
                    "type": "enum",
                    "options": ["relevance", "hot", "top", "new"],
                    "default": "relevance",
                    "description": "How to sort results"
                },
                "time_filter": {
                    "type": "enum",
                    "options": ["all", "year", "month", "week", "day"],
                    "default": "all",
                    "description": "Time period for results"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "range": [1, 100],
                    "description": "Maximum number of results"
                }
            },
            "examples": [] if not include_examples else [
                {"subreddit_name": "MachineLearning", "query": "transformers", "limit": 20},
                {"subreddit_name": "Python", "query": "async", "sort": "top", "time_filter": "month"}
            ]
        },
        "fetch_posts": {
            "description": "Get posts from a single subreddit",
            "parameters": {
                "subreddit_name": {
                    "type": "string",
                    "required": True,
                    "description": "Exact subreddit name (without r/ prefix)"
                },
                "listing_type": {
                    "type": "enum",
                    "options": ["hot", "new", "top", "rising"],
                    "default": "hot",
                    "description": "Type of posts to fetch"
                },
                "time_filter": {
                    "type": "enum",
                    "options": ["all", "year", "month", "week", "day"],
                    "default": None,
                    "description": "Time period (only for 'top' listing)"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "range": [1, 100],
                    "description": "Number of posts to fetch"
                }
            },
            "examples": [] if not include_examples else [
                {"subreddit_name": "technology", "listing_type": "hot", "limit": 15},
                {"subreddit_name": "science", "listing_type": "top", "time_filter": "week", "limit": 20}
            ]
        },
        "fetch_multiple": {
            "description": "Batch fetch from multiple subreddits efficiently",
            "parameters": {
                "subreddit_names": {
                    "type": "array[string]",
                    "required": True,
                    "max_items": 10,
                    "description": "List of subreddit names (without r/ prefix)",
                    "tip": "Use names from discover_subreddits"
                },
                "listing_type": {
                    "type": "enum",
                    "options": ["hot", "new", "top", "rising"],
                    "default": "hot",
                    "description": "Type of posts to fetch"
                },
                "time_filter": {
                    "type": "enum",
                    "options": ["all", "year", "month", "week", "day"],
                    "default": None,
                    "description": "Time period (only for 'top' listing)"
                },
                "limit_per_subreddit": {
                    "type": "integer",
                    "default": 5,
                    "range": [1, 25],
                    "description": "Posts per subreddit"
                }
            },
            "efficiency": {
                "vs_individual": "70% fewer API calls",
                "token_usage": "~500-1000 tokens per subreddit"
            },
            "examples": [] if not include_examples else [
                {"subreddit_names": ["Python", "django", "flask"], "listing_type": "hot", "limit_per_subreddit": 5},
                {"subreddit_names": ["MachineLearning", "deeplearning"], "listing_type": "top", "time_filter": "week", "limit_per_subreddit": 10}
            ]
        },
        "fetch_comments": {
            "description": "Get complete comment tree for a post",
            "parameters": {
                "submission_id": {
                    "type": "string",
                    "required_one_of": ["submission_id", "url"],
                    "description": "Reddit post ID (e.g., '1abc234')"
                },
                "url": {
                    "type": "string",
                    "required_one_of": ["submission_id", "url"],
                    "description": "Full Reddit URL to the post"
                },
                "comment_limit": {
                    "type": "integer",
                    "default": 100,
                    "recommendation": "50-100 for analysis",
                    "description": "Maximum comments to fetch"
                },
                "comment_sort": {
                    "type": "enum",
                    "options": ["best", "top", "new"],
                    "default": "best",
                    "description": "How to sort comments"
                }
            },
            "examples": [] if not include_examples else [
                {"submission_id": "1abc234", "comment_limit": 100},
                {"url": "https://reddit.com/r/Python/comments/xyz789/", "comment_limit": 50, "comment_sort": "top"}
            ]
        }
    }
    
    if operation_id not in schemas:
        return {
            "error": f"Unknown operation: {operation_id}",
            "available": list(schemas.keys()),
            "hint": "Use discover_operations() first"
        }
    
    return schemas[operation_id]


@mcp.tool(
    description="Execute a Reddit operation with validated parameters"
)
def execute_operation(
    operation_id: Annotated[str, "Operation to execute"],
    parameters: Annotated[Dict[str, Any], "Parameters matching the schema"]
) -> Dict[str, Any]:
    """
    LAYER 3: Execute a Reddit operation.
    Only use after getting schema from get_operation_schema.
    """
    # Operation mapping
    operations = {
        "discover_subreddits": discover_subreddits,
        "search_subreddit": search_in_subreddit,
        "fetch_posts": fetch_subreddit_posts,
        "fetch_multiple": fetch_multiple_subreddits,
        "fetch_comments": fetch_submission_with_comments
    }
    
    if operation_id not in operations:
        return {
            "success": False,
            "error": f"Unknown operation: {operation_id}",
            "available_operations": list(operations.keys())
        }
    
    try:
        # Only add reddit client for operations that need it
        if operation_id in ["search_subreddit", "fetch_posts", "fetch_multiple", "fetch_comments"]:
            params = {**parameters, "reddit": reddit}
        else:
            params = parameters
        
        # Execute operation
        result = operations[operation_id](**params)
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "recovery": suggest_recovery(operation_id, e)
        }


def suggest_recovery(operation_id: str, error: Exception) -> str:
    """Helper to suggest recovery actions based on error type."""
    error_str = str(error).lower()
    
    if "not found" in error_str or "404" in error_str:
        return "Verify the subreddit name or use discover_subreddits"
    elif "rate" in error_str or "429" in error_str:
        return "Rate limited - reduce limit parameter or wait before retrying"
    elif "private" in error_str or "403" in error_str:
        return "Subreddit is private - try other communities"
    elif "invalid" in error_str or "validation" in error_str:
        return "Check parameters match schema from get_operation_schema"
    else:
        return "Check parameters match schema from get_operation_schema"


def main():
    """Main entry point for the Reddit MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()