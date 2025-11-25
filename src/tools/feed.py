"""Feed API operations for MCP server.

Provides CRUD operations for feeds via the frontend API,
forwarding the user's Descope authentication token.
"""

import os
from typing import Dict, Any, Optional, List
import httpx
from fastmcp import Context
from fastmcp.server.dependencies import get_http_headers


# API configuration
def get_api_base_url() -> str:
    """Get the Feed API base URL from environment."""
    return os.getenv("AUDIENCE_API_URL", "http://localhost:3001/api")


def get_auth_headers() -> Dict[str, str]:
    """Extract authorization header from the current request context."""
    headers = get_http_headers()
    auth_header = headers.get("authorization", "")
    return {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }


async def create_feed(
    name: str,
    selected_subreddits: list,
    website_url: Optional[str] = None,
    analysis: Optional[Dict[str, Any]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Create a new feed.

    Args:
        name: Name for the feed (1-255 chars)
        selected_subreddits: List of subreddit options with name, description, subscribers, confidence_score
        website_url: URL of the website being analyzed (optional)
        analysis: Feed analysis with description, audience_personas, keywords (optional)
        ctx: FastMCP context (optional)

    Returns:
        Created feed with id, timestamps, etc.
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    payload = {
        "name": name,
        "selected_subreddits": selected_subreddits
    }

    if website_url is not None:
        payload["website_url"] = website_url
    if analysis is not None:
        payload["analysis"] = analysis

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{base_url}/feeds",
                json=payload,
                headers=auth_headers
            )

            if response.status_code == 201:
                return response.json()
            elif response.status_code == 401:
                return {
                    "error": "Authentication required",
                    "suggestion": "Ensure you are authenticated with valid Descope credentials"
                }
            elif response.status_code == 422:
                error_data = response.json()
                return {
                    "error": "Validation error",
                    "details": error_data.get("details", error_data),
                    "suggestion": "Check that all required fields meet validation requirements"
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except httpx.TimeoutException:
            return {
                "error": "Request timeout",
                "suggestion": "The API server may be unavailable. Try again later."
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request failed: {str(e)}",
                "suggestion": "Check that AUDIENCE_API_URL is correctly configured"
            }


async def list_feeds(
    limit: int = 50,
    offset: int = 0,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    List all feeds for the authenticated user.

    Args:
        limit: Maximum number of feeds to return (1-100, default 50)
        offset: Number of feeds to skip (default 0)
        ctx: FastMCP context (optional)

    Returns:
        List of feeds with pagination metadata
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    params = {
        "limit": str(limit),
        "offset": str(offset)
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{base_url}/feeds",
                params=params,
                headers=auth_headers
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {
                    "error": "Authentication required",
                    "suggestion": "Ensure you are authenticated with valid Descope credentials"
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except httpx.TimeoutException:
            return {
                "error": "Request timeout",
                "suggestion": "The API server may be unavailable. Try again later."
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request failed: {str(e)}",
                "suggestion": "Check that AUDIENCE_API_URL is correctly configured"
            }


async def get_feed(
    feed_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get a specific feed by ID.

    Args:
        feed_id: UUID of the feed to retrieve
        ctx: FastMCP context (optional)

    Returns:
        The feed data
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{base_url}/feeds/{feed_id}",
                headers=auth_headers
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {
                    "error": "Authentication required",
                    "suggestion": "Ensure you are authenticated with valid Descope credentials"
                }
            elif response.status_code == 404:
                return {
                    "error": f"Feed not found: {feed_id}",
                    "suggestion": "Use list_feeds to see available feeds"
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except httpx.TimeoutException:
            return {
                "error": "Request timeout",
                "suggestion": "The API server may be unavailable. Try again later."
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request failed: {str(e)}",
                "suggestion": "Check that AUDIENCE_API_URL is correctly configured"
            }


async def update_feed(
    feed_id: str,
    name: Optional[str] = None,
    website_url: Optional[str] = None,
    analysis: Optional[Dict[str, Any]] = None,
    selected_subreddits: Optional[list] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Update an existing feed (partial update).

    Args:
        feed_id: UUID of the feed to update
        name: New name for the feed (optional)
        website_url: Updated website URL (optional)
        analysis: Updated feed analysis (optional)
        selected_subreddits: Updated list of subreddits (optional)
        ctx: FastMCP context (optional)

    Returns:
        The updated feed data
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    # Build payload with only provided fields
    payload = {}
    if name is not None:
        payload["name"] = name
    if website_url is not None:
        payload["website_url"] = website_url
    if analysis is not None:
        payload["analysis"] = analysis
    if selected_subreddits is not None:
        payload["selected_subreddits"] = selected_subreddits

    if not payload:
        return {
            "error": "No fields to update",
            "suggestion": "Provide at least one field to update: name, website_url, analysis, or selected_subreddits"
        }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.put(
                f"{base_url}/feeds/{feed_id}",
                json=payload,
                headers=auth_headers
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {
                    "error": "Authentication required",
                    "suggestion": "Ensure you are authenticated with valid Descope credentials"
                }
            elif response.status_code == 404:
                return {
                    "error": f"Feed not found: {feed_id}",
                    "suggestion": "Use list_feeds to see available feeds"
                }
            elif response.status_code == 422:
                error_data = response.json()
                return {
                    "error": "Validation error",
                    "details": error_data.get("details", error_data),
                    "suggestion": "Check that all fields meet validation requirements"
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except httpx.TimeoutException:
            return {
                "error": "Request timeout",
                "suggestion": "The API server may be unavailable. Try again later."
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request failed: {str(e)}",
                "suggestion": "Check that AUDIENCE_API_URL is correctly configured"
            }


async def delete_feed(
    feed_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Delete a feed.

    Args:
        feed_id: UUID of the feed to delete
        ctx: FastMCP context (optional)

    Returns:
        Confirmation of deletion
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.delete(
                f"{base_url}/feeds/{feed_id}",
                headers=auth_headers
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {
                    "error": "Authentication required",
                    "suggestion": "Ensure you are authenticated with valid Descope credentials"
                }
            elif response.status_code == 404:
                return {
                    "error": f"Feed not found: {feed_id}",
                    "suggestion": "Use list_feeds to see available feeds"
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except httpx.TimeoutException:
            return {
                "error": "Request timeout",
                "suggestion": "The API server may be unavailable. Try again later."
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request failed: {str(e)}",
                "suggestion": "Check that AUDIENCE_API_URL is correctly configured"
            }


async def get_feed_config(
    feed_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get configuration for a feed.

    Args:
        feed_id: UUID of the feed to get config for
        ctx: FastMCP context (optional)

    Returns:
        Feed configuration with subreddit names
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{base_url}/feeds/{feed_id}/config",
                headers=auth_headers
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {
                    "error": "Authentication required",
                    "suggestion": "Ensure you are authenticated with valid Descope credentials"
                }
            elif response.status_code == 404:
                return {
                    "error": f"Feed not found: {feed_id}",
                    "suggestion": "Use list_feeds to see available feeds"
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except httpx.TimeoutException:
            return {
                "error": "Request timeout",
                "suggestion": "The API server may be unavailable. Try again later."
            }
        except httpx.RequestError as e:
            return {
                "error": f"Request failed: {str(e)}",
                "suggestion": "Check that AUDIENCE_API_URL is correctly configured"
            }
