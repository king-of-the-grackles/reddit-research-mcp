# Minimal Chroma Proxy Architecture

## Problem
- You have a Chroma DB with 20,000+ indexed subreddits
- Users need to query it without having your credentials
- MCP server code must stay open source

## Solution
Create a minimal proxy service that handles Chroma queries. Users talk to your proxy, proxy talks to Chroma.

```
User → MCP Server → Your Proxy → Your Chroma DB
```

## Implementation

### Part 1: Proxy Service (Private Repo for Render)

Create a new private repository with just 2 files:

#### `server.py`
```python
from fastapi import FastAPI, HTTPException
import chromadb
import os

app = FastAPI()

# Connect to your Chroma DB
client = chromadb.CloudClient(
    api_key=os.getenv('CHROMA_API_KEY'),
    tenant=os.getenv('CHROMA_TENANT'),
    database=os.getenv('CHROMA_DATABASE')
)

@app.post("/query")
async def query(query_texts: list[str], n_results: int = 10):
    """Simple proxy for Chroma queries."""
    try:
        collection = client.get_collection("reddit_subreddits")
        return collection.query(query_texts=query_texts, n_results=n_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
```

#### `requirements.txt`
```
fastapi
chromadb
uvicorn
```

### Part 2: Update MCP Server (Open Source Repo)

#### Add ONE new file: `src/chroma_proxy.py`
```python
"""Minimal proxy client for Chroma DB access."""
import os
import requests

class ChromaProxyClient:
    """Proxy client that mimics ChromaDB interface."""
    
    def __init__(self):
        self.url = os.getenv('CHROMA_PROXY_URL', 'https://your-reddit-proxy.onrender.com')
    
    def query(self, query_texts, n_results=10):
        """Query through proxy."""
        response = requests.post(
            f"{self.url}/query", 
            json={"query_texts": query_texts, "n_results": n_results},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def list_collections(self):
        """Compatibility method."""
        return [{"name": "reddit_subreddits"}]
    
    def count(self):
        """Compatibility method."""
        return 20000  # Known count

class ProxyCollection:
    """Wrapper to match Chroma collection interface."""
    
    def __init__(self, client):
        self.client = client
    
    def query(self, query_texts, n_results=10):
        return self.client.query(query_texts, n_results)
    
    def count(self):
        return self.client.count()
```

#### Update `src/chroma_client.py` (modify 2 functions only):

1. Update `get_chroma_client()`:
```python
def get_chroma_client():
    """Get ChromaDB client - proxy if no credentials, direct if available."""
    global _client_instance
    
    if _client_instance is not None:
        return _client_instance
    
    # If no direct credentials, use proxy
    if not os.getenv('CHROMA_API_KEY'):
        from .chroma_proxy import ChromaProxyClient
        print("Using proxy for vector database")
        _client_instance = ChromaProxyClient()
        return _client_instance
    
    # Rest of existing code for direct connection...
    config = get_chroma_config()
    # ... existing CloudClient code ...
```

2. Update `get_collection()`:
```python
def get_collection(collection_name="reddit_subreddits", client=None):
    """Get collection - handle both proxy and direct clients."""
    if client is None:
        client = get_chroma_client()
    
    # Handle proxy client
    from .chroma_proxy import ChromaProxyClient, ProxyCollection
    if isinstance(client, ChromaProxyClient):
        return ProxyCollection(client)
    
    # Rest of existing code for direct client...
    try:
        return client.get_collection(collection_name)
    # ... existing error handling ...
```

#### Update `Dockerfile` (add 1 line before CMD):
```dockerfile
# Add this line near the end, before CMD
ENV CHROMA_PROXY_URL=https://your-reddit-proxy.onrender.com
```

#### Update `pyproject.toml` (ensure requests is in dependencies):
```toml
dependencies = [
    # ... existing dependencies ...
    "requests>=2.31.0",  # Add if not present
]
```

### Part 3: Deploy to Render

#### Deploy the Proxy:

1. Push proxy code to private GitHub repo
2. In Render Dashboard:
   - New → Web Service
   - Connect your private repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variables:
     - `CHROMA_API_KEY` = your-key
     - `CHROMA_TENANT` = your-tenant  
     - `CHROMA_DATABASE` = your-database
3. Deploy and note the URL (e.g., `https://reddit-proxy-abc.onrender.com`)

#### Update MCP Server:

1. Change the proxy URL in `Dockerfile` to your Render URL
2. Commit and push to GitHub
3. Deploy to Smithery

## That's It!

Total changes:
- **New files**: 1 proxy client file
- **Modified files**: 2 functions in chroma_client.py, 1 line in Dockerfile
- **Unchanged**: discover.py and all other tool files work as-is

## How It Works

1. When `discover.py` calls `get_chroma_client()`:
   - If no Chroma credentials → returns proxy client
   - If credentials present → returns direct client

2. Proxy client mimics Chroma's `query()` interface exactly

3. Users only need Reddit credentials, vector search "just works"

## Testing Locally

```bash
# Test proxy
cd reddit-proxy
CHROMA_API_KEY=xxx CHROMA_TENANT=yyy CHROMA_DATABASE=zzz uvicorn server:app --reload

# Test MCP with proxy
cd reddit-mcp-poc
CHROMA_PROXY_URL=http://localhost:8000 python src/server.py
```

## Cost & Security Notes

- Render free tier works fine for testing
- Add rate limiting later if needed
- Proxy only exposes one endpoint (`/query`)
- No user authentication needed initially (can add later)

## Why This Approach

- **Minimal**: ~50 lines of new code total
- **No breaking changes**: discover.py unchanged
- **Simple deployment**: 2 files to Render, done
- **Flexible**: Users with own Chroma can still use direct connection
- **Secure**: Your credentials never exposed