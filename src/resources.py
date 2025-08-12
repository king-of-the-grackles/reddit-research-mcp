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
        return {
            "name": "Reddit MCP Server",
            "version": "0.1.0",
            "description": "A Model Context Protocol server for Reddit content access",
            "capabilities": {
                "tools": [
                    {
                        "name": "search_reddit_tool",
                        "description": "Search Reddit content across all subreddits or specific ones",
                        "parameters": ["query", "subreddit", "sort", "time_filter", "limit"]
                    },
                    {
                        "name": "fetch_subreddit_posts_tool",
                        "description": "Get posts from a specific subreddit",
                        "parameters": ["subreddit_name", "listing_type", "time_filter", "limit"]
                    },
                    {
                        "name": "fetch_submission_with_comments_tool",
                        "description": "Get a Reddit post with its comment tree",
                        "parameters": ["submission_id or url", "comment_limit", "comment_sort"]
                    }
                ],
                "resources": [
                    {
                        "uri": "reddit://popular-subreddits",
                        "description": "List of 25 most popular subreddits"
                    },
                    {
                        "uri": "reddit://subreddit/{name}/about",
                        "description": "Detailed information about a specific subreddit"
                    },
                    {
                        "uri": "reddit://server-info",
                        "description": "Information about this MCP server"
                    }
                ]
            },
            "usage_examples": {
                "search": "search_reddit_tool(query='python programming', sort='top', limit=10)",
                "fetch_posts": "fetch_subreddit_posts_tool(subreddit_name='technology', listing_type='hot')",
                "get_comments": "fetch_submission_with_comments_tool(url='https://reddit.com/r/...')",
                "get_subreddit_info": "Access resource: reddit://subreddit/python/about"
            },
            "rate_limiting": "Handled automatically by PRAW with 5-minute cooldown",
            "authentication": "Application-only (read-only access)"
        }