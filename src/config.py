import praw
import os
from dotenv import load_dotenv

load_dotenv()

def get_reddit_client() -> praw.Reddit:
    """Get configured Reddit client (read-only)."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "RedditMCP/1.0")
    
    if not client_id or not client_secret:
        raise ValueError(
            "Reddit API credentials not found. Please set REDDIT_CLIENT_ID "
            "and REDDIT_CLIENT_SECRET in your .env file"
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