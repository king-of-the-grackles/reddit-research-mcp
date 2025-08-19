#!/usr/bin/env python3
"""Verify that all indexed subreddits meet the 5000 subscriber minimum"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.config import Settings

def verify_subscriber_filter():
    # Initialize ChromaDB client
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client = chromadb.PersistentClient(
        path=os.path.join(script_dir, "data", "subreddit_vectors"),
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get collection
    collection = client.get_collection("reddit_subreddits")
    
    print("Verifying subscriber filter (minimum: 5,000)...")
    print(f"Total indexed subreddits: {collection.count()}\n")
    
    # Get all documents with metadata
    results = collection.get(include=["metadatas"])
    
    # Check each subreddit's subscriber count
    below_threshold = []
    subscriber_counts = []
    
    print("Subreddit subscriber counts:")
    print("-" * 50)
    
    for metadata in results['metadatas']:
        name = metadata.get('name', 'Unknown')
        subscribers = metadata.get('subscribers', 0)
        subscriber_counts.append(subscribers)
        
        status = "✅" if subscribers >= 5000 else "❌"
        print(f"{status} r/{name:<30} {subscribers:>12,} subscribers")
        
        if subscribers < 5000:
            below_threshold.append((name, subscribers))
    
    print("-" * 50)
    
    # Statistics
    if subscriber_counts:
        min_subs = min(subscriber_counts)
        max_subs = max(subscriber_counts)
        avg_subs = sum(subscriber_counts) / len(subscriber_counts)
        
        print(f"\nStatistics:")
        print(f"  Minimum: {min_subs:,} subscribers")
        print(f"  Maximum: {max_subs:,} subscribers")
        print(f"  Average: {avg_subs:,.0f} subscribers")
    
    # Report results
    print(f"\nFilter verification results:")
    if below_threshold:
        print(f"❌ FAILED: {len(below_threshold)} subreddits below 5,000 threshold:")
        for name, count in below_threshold:
            print(f"   - r/{name}: {count:,} subscribers")
    else:
        print("✅ PASSED: All subreddits have 5,000+ subscribers")
    
    return len(below_threshold) == 0

if __name__ == "__main__":
    success = verify_subscriber_filter()
    exit(0 if success else 1)