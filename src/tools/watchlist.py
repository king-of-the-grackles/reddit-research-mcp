"""Watchlist API operations for MCP server.

Provides CRUD operations for watchlists via the frontend API,
forwarding the user's Descope authentication token.
"""

import os
from typing import Dict, Any, Optional, List
import httpx
from fastmcp import Context
from fastmcp.server.dependencies import get_http_headers


# API configuration
def get_api_base_url() -> str:
    """Get the Watchlist API base URL from environment."""
    return os.getenv("AUDIENCE_API_URL", "http://localhost:3001/api")


def get_auth_headers() -> Dict[str, str]:
    """Extract authorization header from the current request context."""
    headers = get_http_headers()
    auth_header = headers.get("authorization", "")
    return {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }


async def create_watchlist(
    name: str,
    selected_subreddits: list,
    website_url: Optional[str] = None,
    analysis: Optional[Dict[str, Any]] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Create a new watchlist.

    Args:
        name: Name for the watchlist (1-255 chars)
        selected_subreddits: List of subreddit options with name, description, subscribers, confidence_score
        website_url: URL of the website being analyzed (optional)
        analysis: Watchlist analysis with description, audience_personas, keywords (optional)
        ctx: FastMCP context (optional)

    Returns:
        Created watchlist with id, timestamps, etc.
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
                f"{base_url}/watchlist",
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


async def list_watchlists(
    limit: int = 50,
    offset: int = 0,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    List all watchlists for the authenticated user.

    Args:
        limit: Maximum number of watchlists to return (1-100, default 50)
        offset: Number of watchlists to skip (default 0)
        ctx: FastMCP context (optional)

    Returns:
        List of watchlists with pagination metadata
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
                f"{base_url}/watchlist",
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


async def get_watchlist(
    watchlist_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Get a specific watchlist by ID.

    Args:
        watchlist_id: UUID of the watchlist to retrieve
        ctx: FastMCP context (optional)

    Returns:
        The watchlist data
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{base_url}/watchlist/{watchlist_id}",
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
                    "error": f"Watchlist not found: {watchlist_id}",
                    "suggestion": "Use list_watchlists to see available watchlists"
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


async def update_watchlist(
    watchlist_id: str,
    name: Optional[str] = None,
    website_url: Optional[str] = None,
    analysis: Optional[Dict[str, Any]] = None,
    selected_subreddits: Optional[list] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Update an existing watchlist (partial update).

    Args:
        watchlist_id: UUID of the watchlist to update
        name: New name for the watchlist (optional)
        website_url: Updated website URL (optional)
        analysis: Updated watchlist analysis (optional)
        selected_subreddits: Updated list of subreddits (optional)
        ctx: FastMCP context (optional)

    Returns:
        The updated watchlist data
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
                f"{base_url}/watchlist/{watchlist_id}",
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
                    "error": f"Watchlist not found: {watchlist_id}",
                    "suggestion": "Use list_watchlists to see available watchlists"
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


async def delete_watchlist(
    watchlist_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Delete a watchlist.

    Args:
        watchlist_id: UUID of the watchlist to delete
        ctx: FastMCP context (optional)

    Returns:
        Confirmation of deletion
    """
    base_url = get_api_base_url()
    auth_headers = get_auth_headers()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.delete(
                f"{base_url}/watchlist/{watchlist_id}",
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
                    "error": f"Watchlist not found: {watchlist_id}",
                    "suggestion": "Use list_watchlists to see available watchlists"
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
