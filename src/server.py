from fastmcp import FastMCP
from fastmcp.prompts import Message
from typing import Optional, Literal, List, Union, Dict, Any, Annotated
import sys
import os
import json
from pathlib import Path
from datetime import datetime

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

# Initialize Reddit client (will be updated with config when available)
reddit = None


def initialize_reddit_client():
    """Initialize Reddit client with environment config."""
    global reddit
    reddit = get_reddit_client()
    # Register resources with the new client
    register_resources(mcp, reddit)

# Initialize with environment variables initially
try:
    initialize_reddit_client()
except Exception as e:
    print(f"DEBUG: Reddit init failed: {e}", flush=True)


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


# Research Workflow Prompt Template
RESEARCH_WORKFLOW_PROMPT = """
You are conducting comprehensive Reddit research based on this request: "{research_request}"

## WORKFLOW TO FOLLOW:

### PHASE 1: DISCOVERY
1. First, call discover_operations() to see available operations
2. Then call get_operation_schema("discover_subreddits") to understand the parameters
3. Extract the key topic/question from the research request and execute:
   execute_operation("discover_subreddits", {{"query": "<topic from request>", "limit": 15}})
4. Note the confidence scores for each discovered subreddit

### PHASE 2: STRATEGY SELECTION
Based on confidence scores from discovery:
- **High confidence (>0.7)**: Focus on top 5-8 most relevant subreddits
- **Medium confidence (0.4-0.7)**: Cast wider net with 10-12 subreddits  
- **Low confidence (<0.4)**: Refine search terms and retry discovery

### PHASE 3: GATHER POSTS
Use batch operation for efficiency:
execute_operation("fetch_multiple", {{
    "subreddit_names": [<list from discovery>],
    "listing_type": "top",
    "time_filter": "year",
    "limit_per_subreddit": 10
}})

### PHASE 4: DEEP DIVE INTO DISCUSSIONS
For posts with high engagement (10+ comments, 5+ upvotes):
execute_operation("fetch_comments", {{
    "submission_id": "<post_id>",
    "comment_limit": 100,
    "comment_sort": "best"
}})

Target: Analyze 100+ total comments across 10+ subreddits

### PHASE 5: SYNTHESIZE FINDINGS

Create a comprehensive report that directly addresses the research request:

# Research Report: {research_request}
*Generated: {timestamp}*

## Executive Summary
- Direct answer to the research question
- Key findings with confidence levels
- Coverage metrics: X subreddits, Y posts, Z comments analyzed

## Communities Analyzed
| Subreddit | Subscribers | Relevance Score | Posts Analyzed | Key Insights |
|-----------|------------|-----------------|----------------|--------------|
| [data]    | [count]    | [0.0-1.0]      | [count]        | [summary]    |

## Key Findings

### [Finding that directly addresses the research request]
**Community Consensus**: [Strong/Moderate/Split/Emerging]

Evidence from Reddit:
- u/[username] in r/[subreddit] stated: "exact quote" [↑450](https://reddit.com/r/subreddit/comments/abc123/)
- Discussion with 200+ comments shows... [link](url)
- Highly awarded post argues... [↑2.3k, Gold×3](url)

### [Additional relevant findings...]
[Continue with 2-4 more key findings that answer different aspects of the research request]

## Temporal Trends
- How perspectives have evolved over time
- Recent shifts in community sentiment
- Emerging viewpoints in the last 30 days

## Notable Perspectives
- Expert opinions (verified flairs, high karma users 10k+)
- Contrarian views worth considering
- Common misconceptions identified

## Data Quality Metrics
- Total subreddits analyzed: [count]
- Total posts reviewed: [count]
- Total comments analyzed: [count]  
- Unique contributors: [count]
- Date range: [oldest] to [newest]
- Average post score: [score]
- High-karma contributors (10k+): [count]

## Limitations
- Geographic/language bias (primarily English-speaking communities)
- Temporal coverage (data from [date range])
- Communities not represented in analysis

---
*Research methodology: Semantic discovery across 20,000+ indexed subreddits, followed by deep analysis of high-engagement discussions*

CRITICAL REQUIREMENTS:
- Never fabricate Reddit content - only cite actual posts/comments from the data
- Every claim must link to its Reddit source with a clickable URL
- Include upvote counts and awards for credibility assessment
- Note when content is [deleted] or [removed]
- Track temporal context (when was this posted?)
- Answer the specific research request - don't just summarize content
"""


@mcp.prompt(
    name="reddit_research",
    description="Conduct comprehensive Reddit research on any topic or question",
    tags={"research", "analysis", "comprehensive"}
)
def reddit_research(research_request: str) -> List[Message]:
    """
    Guides comprehensive Reddit research based on a natural language request.
    
    Args:
        research_request: Natural language description of what to research
                         Examples: "How do people feel about remote work?",
                                 "Best practices for Python async programming",
                                 "Community sentiment on electric vehicles"
    
    Returns:
        Structured messages guiding the LLM through the complete research workflow
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    return [
        Message(
            role="assistant", 
            content=RESEARCH_WORKFLOW_PROMPT.format(
                research_request=research_request,
                timestamp=timestamp
            )
        ),
        Message(
            role="user",
            content=f"Please conduct comprehensive Reddit research to answer: {research_request}"
        )
    ]


def main():
    """Main entry point for the server."""
    print("Reddit MCP Server starting...", flush=True)
    
    # Try to initialize the Reddit client with available configuration
    try:
        initialize_reddit_client()
        print("Reddit client initialized successfully", flush=True)
    except Exception as e:
        print(f"WARNING: Failed to initialize Reddit client: {e}", flush=True)
        print("Server will run with limited functionality.", flush=True)
        print("\nPlease provide Reddit API credentials via:", flush=True)
        print("  1. Environment variables: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT", flush=True)
        print("  2. Config file: .mcp-config.json", flush=True)
    
    # Run with stdio transport
    mcp.run()


if __name__ == "__main__":
    main()