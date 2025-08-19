#!/usr/bin/env python3
"""Test script to validate indexed data"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.config import Settings
from pathlib import Path
import json

def test_indexed_data():
    # Initialize ChromaDB client
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client = chromadb.PersistentClient(
        path=os.path.join(script_dir, "data", "subreddit_vectors"),
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get collection
    collection = client.get_collection("reddit_subreddits")
    
    print("Testing ChromaDB Collection...")
    print(f"Collection name: {collection.name}")
    print(f"Total documents: {collection.count()}")
    
    # Get all documents
    results = collection.get(include=["documents", "metadatas"])
    
    print("\n--- Sample Document Analysis ---")
    if results['documents']:
        # Check first document
        first_doc = results['documents'][0]
        first_meta = results['metadatas'][0]
        first_id = results['ids'][0]
        
        print(f"\nDocument ID: {first_id}")
        print(f"Metadata keys: {list(first_meta.keys())}")
        print(f"Subreddit name: r/{first_meta.get('name', 'N/A')}")
        print(f"Subscribers: {first_meta.get('subscribers', 'N/A')}")
        print(f"NSFW: {first_meta.get('nsfw', 'N/A')}")
        print(f"URL: {first_meta.get('url', 'N/A')}")
        print(f"Document text length: {len(first_doc)} characters")
        
        # Validate metadata structure
        required_fields = ['name', 'subscribers', 'nsfw', 'created', 'indexed_at', 'url']
        missing_fields = [f for f in required_fields if f not in first_meta]
        
        if missing_fields:
            print(f"\n⚠️  Missing metadata fields: {missing_fields}")
        else:
            print("\n✅ All required metadata fields present")
        
    # Test semantic search
    print("\n--- Testing Semantic Search ---")
    search_query = "technology programming software development"
    search_results = collection.query(
        query_texts=[search_query],
        n_results=3
    )
    
    print(f"Query: '{search_query}'")
    print(f"Found {len(search_results['ids'][0])} results:")
    
    for i, (doc_id, distance, metadata) in enumerate(zip(
        search_results['ids'][0],
        search_results['distances'][0],
        search_results['metadatas'][0]
    )):
        print(f"\n  Result {i+1}:")
        print(f"    Subreddit: r/{metadata['name']}")
        print(f"    Subscribers: {metadata['subscribers']:,}")
        print(f"    Distance: {distance:.4f}")
        print(f"    URL: {metadata['url']}")
    
    # Load and verify state file
    print("\n--- State File Validation ---")
    state_file = Path(os.path.join(script_dir, "data", "indexer_state.json"))
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        print(f"Last full index: {state.get('last_full_index', 'Never')}")
        print(f"Last update: {state.get('last_update', 'Never')}")
        print(f"Indexed subreddit IDs: {len(state.get('indexed_subreddits', []))}")
        
        # Verify IDs match collection
        indexed_ids = set(state.get('indexed_subreddits', []))
        collection_ids = set(results['ids'])
        
        if indexed_ids == collection_ids:
            print("✅ State file IDs match collection IDs")
        else:
            print("⚠️  State file IDs don't match collection")
            print(f"   In state but not collection: {indexed_ids - collection_ids}")
            print(f"   In collection but not state: {collection_ids - indexed_ids}")
    else:
        print("⚠️  State file not found")
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_indexed_data()