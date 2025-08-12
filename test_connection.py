#!/usr/bin/env python
"""Test Reddit API connection."""

import os
from dotenv import load_dotenv
import praw

load_dotenv()

def test_connection():
    """Test Reddit API connection."""
    print("Testing Reddit API Connection")
    print("=" * 40)
    
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "RedditMCP/1.0")
    
    print(f"Client ID: {client_id[:10]}..." if client_id else "Missing")
    print(f"User Agent: {user_agent}")
    
    try:
        # Create Reddit instance with read-only mode
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            redirect_uri="http://localhost:8080"
        )
        
        # Enable read-only mode
        reddit.read_only = True
        
        print("\nAttempting to connect to Reddit API...")
        
        # Test by fetching a post from r/python
        subreddit = reddit.subreddit("python")
        
        for submission in subreddit.hot(limit=1):
            print(f"\n✅ SUCCESS! Reddit API is working!")
            print(f"Sample post from r/python:")
            print(f"  Title: {submission.title[:60]}...")
            print(f"  Score: {submission.score}")
            print(f"  Comments: {submission.num_comments}")
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n🎉 Your Reddit MCP server is ready to use!")
        print("Run: uv run fastmcp dev src/server.py:mcp")