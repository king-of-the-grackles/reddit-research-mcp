"""
ChromaDB Cloud client for Reddit MCP.

Provides connection to ChromaDB Cloud for vector storage and retrieval.
"""

import os
import chromadb
from typing import Optional
from datetime import datetime


_client_instance = None


def get_chroma_config() -> dict:
    """
    Load ChromaDB Cloud configuration from environment variables.
    
    Returns:
        Dictionary with ChromaDB Cloud configuration
    """
    return {
        'api_key': os.getenv('CHROMA_API_KEY'),
        'tenant': os.getenv('CHROMA_TENANT'),
        'database': os.getenv('CHROMA_DATABASE')
    }


def get_chroma_client() -> chromadb.CloudClient:
    """
    Get ChromaDB Cloud client instance (singleton pattern).
    
    Returns:
        ChromaDB CloudClient instance
    
    Raises:
        ValueError: If cloud credentials are missing
        ConnectionError: If unable to connect to ChromaDB Cloud
    """
    global _client_instance
    
    # Return cached instance if available
    if _client_instance is not None:
        return _client_instance
    
    config = get_chroma_config()
    
    # Validate cloud credentials
    if not all([config['api_key'], config['tenant'], config['database']]):
        raise ValueError(
            "ChromaDB Cloud credentials incomplete. "
            "Please set CHROMA_API_KEY, CHROMA_TENANT, and CHROMA_DATABASE"
        )
    
    try:
        print(f"🌩️  Connecting to ChromaDB Cloud (database: {config['database']})")
        
        # Create CloudClient
        client = chromadb.CloudClient(
            api_key=config['api_key'],
            tenant=config['tenant'],
            database=config['database']
        )
        
        # Cache the instance
        _client_instance = client
        return client
        
    except Exception as e:
        raise ConnectionError(f"Failed to connect to ChromaDB Cloud: {e}")


def reset_client_cache():
    """Reset the cached client instance (useful for testing)."""
    global _client_instance
    _client_instance = None


def get_collection(
    collection_name: str = "reddit_subreddits",
    client: Optional[chromadb.CloudClient] = None
):
    """
    Get or create a ChromaDB collection.
    
    Args:
        collection_name: Name of the collection
        client: Optional client instance (uses default if not provided)
    
    Returns:
        ChromaDB collection instance
    """
    if client is None:
        client = get_chroma_client()
    
    try:
        # Try to get existing collection
        return client.get_collection(collection_name)
    except Exception:
        # Create new collection if it doesn't exist
        print(f"📝 Creating new collection: {collection_name}")
        return client.create_collection(
            name=collection_name,
            metadata={
                "description": "Reddit subreddits for semantic search",
                "source": "reddit-mcp",
                "created": datetime.now().isoformat()
            }
        )


def test_connection() -> dict:
    """
    Test ChromaDB Cloud connection and return status information.
    
    Returns:
        Dictionary with connection status and details
    """
    status = {
        'mode': 'cloud',
        'connected': False,
        'error': None,
        'collections': [],
        'document_count': 0
    }
    
    try:
        client = get_chroma_client()
        
        # Test by listing collections
        collections = client.list_collections()
        status['connected'] = True
        status['collections'] = [col.name for col in collections]
        
        # Get document count from main collection if it exists
        try:
            collection = client.get_collection("reddit_subreddits")
            status['document_count'] = collection.count()
        except:
            pass
        
    except Exception as e:
        status['error'] = str(e)
    
    return status