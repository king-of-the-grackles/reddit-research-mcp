#!/usr/bin/env python3
"""Test that simplified embeddings still work for search"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.config import Settings

def test_search():
    # Initialize ChromaDB client
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client = chromadb.PersistentClient(
        path=os.path.join(script_dir, "data", "subreddit_vectors"),
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get collection
    collection = client.get_collection("reddit_subreddits")
    
    print(f"Collection has {collection.count()} subreddits")
    
    # Test searches
    test_queries = [
        "gaming video games",
        "technology programming",
        "funny memes humor",
        "movies films entertainment"
    ]
    
    for query in test_queries:
        print(f"\n--- Search: '{query}' ---")
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        
        for i, (meta, distance) in enumerate(zip(
            results['metadatas'][0],
            results['distances'][0]
        )):
            print(f"  {i+1}. r/{meta['name']} ({meta['subscribers']:,} subs) - distance: {distance:.3f}")
    
    print("\n✅ Search still works with simplified embeddings!")

if __name__ == "__main__":
    test_search()