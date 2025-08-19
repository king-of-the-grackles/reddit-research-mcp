import praw
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import parse_qs

def get_reddit_client() -> praw.Reddit:
    """Get configured Reddit client (read-only) with Smithery support."""
    client_id = None
    client_secret = None
    user_agent = None
    
    # Method 1: Try query parameters first (Smithery deployment)
    # Smithery passes config as query params in QUERY_STRING env var
    query_string = os.environ.get('QUERY_STRING', '')
    if query_string:
        params = parse_qs(query_string)
        client_id = params.get('REDDIT_CLIENT_ID', [None])[0]
        client_secret = params.get('REDDIT_CLIENT_SECRET', [None])[0]
        user_agent = params.get('REDDIT_USER_AGENT', ['RedditResearchMCP/1.0 (Smithery)'])[0]
    
    # Method 2: Check OS environment variables
    if not client_id or not client_secret:
        client_id = os.environ.get("REDDIT_CLIENT_ID")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        user_agent = os.environ.get("REDDIT_USER_AGENT", "RedditMCP/1.0")
    
    # Method 3: Try loading from .env file (local development)
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