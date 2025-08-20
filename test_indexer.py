#!/usr/bin/env python3
"""
Test script for the improved Reddit subreddit indexer.
Run this to verify the new discovery methods work correctly.
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

async def test_indexer():
    """Test the improved indexer with a small limit"""
    from src.tools.db.reddit_subreddit_indexer import SubredditIndexer, ACTIVITY_THRESHOLD_DAYS
    
    print("🧪 Testing improved Reddit Subreddit Indexer")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("REDDIT_CLIENT_ID") or not os.getenv("REDDIT_CLIENT_SECRET"):
        print("❌ Error: Reddit API credentials not found")
        print("Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env")
        return
    
    if not os.getenv("CHROMA_API_KEY"):
        print("❌ Error: ChromaDB Cloud credentials not found")
        print("Please set CHROMA_API_KEY, CHROMA_TENANT, and CHROMA_DATABASE in .env")
        return
    
    try:
        # Initialize indexer
        print("📊 Initializing indexer...")
        indexer = SubredditIndexer()
        
        # Get initial stats
        initial_stats = indexer.get_stats()
        print(f"✅ Connected to ChromaDB Cloud")
        print(f"📈 Current collection size: {initial_stats['total_indexed']:,} subreddits")
        print(f"🎯 Min subscribers threshold: {initial_stats['min_subscribers']:,}")
        print(f"📅 Activity threshold: {ACTIVITY_THRESHOLD_DAYS} days")
        print()
        
        # Test with a small limit to verify functionality
        print("🚀 Starting test indexing (limit: 100 for quick test)")
        print("This will test the new discovery methods:")
        print("  1. Default/Gold subreddits")
        print("  2. Popular subreddits") 
        print("  3. Smart prefix search (search_by_name)")
        print("  4. Topic-based search (search_by_topic)")
        print("  5. Recommendation graph")
        print()
        
        # Run the indexer with a small limit
        await indexer.build_full_index(limit=100)
        
        # Get final stats
        final_stats = indexer.get_stats()
        new_subs = final_stats['total_indexed'] - initial_stats['total_indexed']
        
        print()
        print("✅ Test completed successfully!")
        print(f"📊 New subreddits indexed: {new_subs:,}")
        print(f"📈 Total collection size: {final_stats['total_indexed']:,}")
        
        # Cleanup
        await indexer.cleanup()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting indexer test...")
    asyncio.run(test_indexer())