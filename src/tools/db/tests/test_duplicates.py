#!/usr/bin/env python3
"""Test duplicate prevention in the indexer"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reddit_subreddit_indexer import SubredditIndexer

async def test_duplicates():
    indexer = SubredditIndexer()
    
    print(f"Starting with {len(indexer.discovered_ids)} existing IDs")
    print(f"Current collection count: {indexer.collection.count()}")
    
    # Try to discover some popular subreddits (should find duplicates)
    print("\nDiscovering 10 popular subreddits...")
    popular = await indexer.discover_popular_subreddits(limit=10)
    
    print(f"Found {len(popular)} new subreddits")
    print(f"Duplicates avoided: {indexer.duplicates_avoided}")
    
    # Try again to see more duplicates
    print("\nTrying to discover 10 more...")
    indexer.duplicates_avoided = 0  # Reset counter for this test
    more = await indexer.discover_popular_subreddits(limit=10)
    
    print(f"Found {len(more)} new subreddits")
    print(f"Duplicates avoided: {indexer.duplicates_avoided}")
    
    await indexer.cleanup()

if __name__ == "__main__":
    asyncio.run(test_duplicates())