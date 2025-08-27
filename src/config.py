#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "praw>=7.7.1",
#     "python-dotenv>=1.0.0",
#     "langfuse>=2.50.0",
# ]
# ///

import praw
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

def get_reddit_client() -> praw.Reddit:
    """Get configured Reddit client (read-only) from environment."""
    client_id = None
    client_secret = None
    user_agent = None
    
    # Method 1: Try environment variables
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT", "RedditMCP/1.0")
    
    # Method 2: Try loading from .env file (local development)
    if not client_id or not client_secret:
        # Find .env file in project root
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            client_id = os.getenv("REDDIT_CLIENT_ID")
            client_secret = os.getenv("REDDIT_CLIENT_SECRET")
            if not user_agent:
                user_agent = os.getenv("REDDIT_USER_AGENT", "RedditMCP/1.0")
    
    if not client_id or not client_secret:
        raise ValueError(
            "Reddit API credentials not found. Please set REDDIT_CLIENT_ID "
            "and REDDIT_CLIENT_SECRET either as OS environment variables or in a .env file"
        )
    
    # Create Reddit instance for read-only access
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        redirect_uri="http://localhost:8080",  # Required even for read-only
        ratelimit_seconds=300  # Auto-handle rate limits
    )
    
    # Explicitly enable read-only mode
    reddit.read_only = True
    
    return reddit

def get_langfuse_client() -> Optional[object]:
    """Get configured Langfuse client from environment."""
    import os
    
    # Check if observability is explicitly disabled
    if os.environ.get("LANGFUSE_ENABLED", "true").lower() == "false":
        return None
    
    # Get credentials from environment
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    
    # Try loading from .env file if not in environment
    if not public_key or not secret_key:
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
            secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    
    if not public_key or not secret_key:
        # Observability is optional - return None if not configured
        print("Langfuse credentials not found. Observability disabled.", flush=True)
        return None
    
    try:
        from langfuse import Langfuse
        
        langfuse = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            # Optional: configure based on environment
            environment=os.environ.get("LANGFUSE_ENVIRONMENT", "production"),
            release=os.environ.get("LANGFUSE_RELEASE", None),
            debug=os.environ.get("LANGFUSE_DEBUG", "false").lower() == "true"
        )
        
        # Optional: verify connection (not recommended for production)
        if os.environ.get("LANGFUSE_VERIFY_CONNECTION", "false").lower() == "true":
            if langfuse.auth_check():
                print("Langfuse connected successfully", flush=True)
            else:
                print("Langfuse authentication failed", flush=True)
                return None
        
        return langfuse
        
    except ImportError:
        print("Langfuse not installed. Run: pip install langfuse", flush=True)
        return None
    except Exception as e:
        print(f"Failed to initialize Langfuse: {e}", flush=True)
        return None