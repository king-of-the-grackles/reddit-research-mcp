import praw
import os
from pathlib import Path
from dotenv import load_dotenv

def get_reddit_client() -> praw.Reddit:
    """Get configured Reddit client (read-only)."""
    # First check if credentials exist in OS environment
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    
    # If not found in OS env, try loading from .env file
    if not client_id or not client_secret:
        # Find .env file in project root
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            client_id = os.getenv("REDDIT_CLIENT_ID")
            client_secret = os.getenv("REDDIT_CLIENT_SECRET")
            # Credentials loaded silently for security
        else:
            # Silent operation - no debug output
            pass
    else:
        # Credentials loaded from environment - no output needed
        pass
    
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