"""
ChromaDB Cloud client for Reddit MCP.

Provides connection to ChromaDB Cloud for vector storage and retrieval.
"""

import os
import chromadb
from typing import Optional, List, Dict, Any
from datetime import datetime
import requests


_client_instance = None


# ============= PROXY CLIENT CLASSES =============
class ChromaProxyClient:
    """Proxy client that mimics ChromaDB interface."""
    
    def __init__(self, proxy_url: Optional[str] = None):
        self.url = proxy_url or os.getenv(
            'CHROMA_PROXY_URL', 
            'https://reddit-mcp-vector-db.onrender.com'
        )
        self.session = requests.Session()
    
    def query(self, query_texts: List[str], n_results: int = 10) -> Dict[str, Any]:
        """Query through proxy."""
        try:
            response = self.session.post(
                f"{self.url}/query",
                json={"query_texts": query_texts, "n_results": n_results},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to query vector database: {e}")
    
    def list_collections(self) -> List[Dict[str, str]]:
        """Compatibility method."""
        return [{"name": "reddit_subreddits"}]
    
    def count(self) -> int:
        """Get document count."""
        try:
            response = self.session.get(f"{self.url}/stats", timeout=5)
            if response.status_code == 200:
                return response.json().get('total_subreddits', 20000)
        except:
            pass
        return 20000


class ProxyCollection:
    """Wrapper to match Chroma collection interface."""
    
    def __init__(self, proxy_client: ChromaProxyClient):
        self.proxy_client = proxy_client
        self.name = "reddit_subreddits"
    
    def query(self, query_texts: List[str], n_results: int = 10) -> Dict[str, Any]:
        return self.proxy_client.query(query_texts, n_results)
    
    def count(self) -> int:
        return self.proxy_client.count()
# ============= END PROXY CLIENT CLASSES =============


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


def get_chroma_client():
    """
    Get ChromaDB client - uses proxy if no credentials, direct if available.
    
    Returns:
        ChromaDB CloudClient or ChromaProxyClient instance
    
    Raises:
        ConnectionError: If unable to connect to ChromaDB Cloud or proxy
    """
    global _client_instance
    
    # Return cached instance if available
    if _client_instance is not None:
        return _client_instance
    
    config = get_chroma_config()
    
    # Use proxy if no direct credentials
    if not config['api_key']:
        print("🌐 Using proxy for vector database access")
        _client_instance = ChromaProxyClient()
        return _client_instance
    
    # Validate cloud credentials for direct connection
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
    client = None
):
    """
    Get or create a ChromaDB collection.
    
    Args:
        collection_name: Name of the collection
        client: Optional client instance (uses default if not provided)
    
    Returns:
        ChromaDB collection instance or ProxyCollection
    """
    if client is None:
        client = get_chroma_client()
    
    # Handle proxy client
    if isinstance(client, ChromaProxyClient):
        return ProxyCollection(client)
    
    try:
        # Try to get existing collection
        return client.get_collection(collection_name)
    except Exception as e:
        # Check if it's a parsing error (collection exists but with different format)
        if "KeyError" in str(type(e)):
            # Try to get it directly without parsing
            try:
                import chromadb
                # Use low-level API to list collections
                collections = client.list_collections()
                for col in collections:
                    if col.name == collection_name:
                        return col
            except:
                pass
        
        # Try to create new collection
        try:
            print(f"📝 Creating new collection: {collection_name}")
            return client.create_collection(
                name=collection_name,
                metadata={
                    "description": "Reddit subreddits for semantic search",
                    "source": "reddit-mcp",
                    "created": datetime.now().isoformat()
                }
            )
        except Exception as create_error:
            # If creation fails because it already exists, try getting it again
            if "already exists" in str(create_error):
                # Force get with simpler approach
                return client.get_or_create_collection(name=collection_name)
            raise create_error


def test_connection() -> dict:
    """
    Test ChromaDB connection and return status information.
    
    Returns:
        Dictionary with connection status and details
    """
    status = {
        'mode': 'unknown',
        'connected': False,
        'error': None,
        'collections': [],
        'document_count': 0
    }
    
    try:
        client = get_chroma_client()
        
        # Determine mode
        if isinstance(client, ChromaProxyClient):
            status['mode'] = 'proxy'
            status['connected'] = True
            status['collections'] = ['reddit_subreddits']
            status['document_count'] = client.count()
        else:
            status['mode'] = 'cloud'
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