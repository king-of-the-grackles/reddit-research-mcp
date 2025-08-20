#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "asyncpraw>=7.7.0",
#     "chromadb>=0.4.0",
#     "python-dotenv>=1.0.0",
#     "tqdm>=4.66.0",
#     "rich>=13.0.0",
#     "aiofiles>=23.0.0"
# ]
# ///
"""
Reddit Subreddit ChromaDB Indexer

Discovers and indexes all active Reddit subreddits into ChromaDB for semantic search.

Usage:
    # Build complete index (first time or rebuild)
    ./reddit_subreddit_indexer.py --build
    
    # Update existing index (incremental)
    ./reddit_subreddit_indexer.py --update
    
    # Check index status
    ./reddit_subreddit_indexer.py --status
    
    # Test with limited subreddits
    ./reddit_subreddit_indexer.py --build --limit 1000
"""

import asyncio
import asyncpraw
import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
import argparse
from tqdm.asyncio import tqdm
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import aiofiles
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from src.chroma_client import get_chroma_client, get_collection
except ImportError:
    # If running as a script directly
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
    from src.chroma_client import get_chroma_client, get_collection

# Load environment
load_dotenv()

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COLLECTION_NAME = "reddit_subreddits"
STATE_FILE = os.path.join(SCRIPT_DIR, "data", "indexer_state.json")
BATCH_SIZE = 100
ACTIVITY_THRESHOLD_DAYS = 7  # Reduced from 30 to capture more recently active subreddits
MIN_SUBSCRIBERS = 2000  # Reduced from 5000 to capture more communities

console = Console()

class StreamingDiscoveryCollector:
    """Collects and indexes subreddits in batches to minimize memory usage"""
    
    def __init__(self, indexer, batch_size: int = 500):
        self.indexer = indexer
        self.batch_size = batch_size
        self.current_batch = []
        self.seen_ids = set(indexer.discovered_ids)  # Only store IDs, not full data
        self.total_collected = 0
        self.total_indexed = 0
        self.duplicates_skipped = 0
        self.batch_count = 0
        
    async def add(self, subreddit_data: Dict) -> bool:
        """Add a subreddit to the collector, auto-flushing when batch is full"""
        if not subreddit_data or subreddit_data['id'] in self.seen_ids:
            self.duplicates_skipped += 1
            return False
        
        self.seen_ids.add(subreddit_data['id'])
        self.current_batch.append(subreddit_data)
        self.total_collected += 1
        
        # Auto-flush when batch is full
        if len(self.current_batch) >= self.batch_size:
            await self.flush()
        
        return True
    
    async def flush(self):
        """Index current batch and clear memory"""
        if not self.current_batch:
            return
        
        self.batch_count += 1
        batch_size = len(self.current_batch)
        
        # Index the batch
        await self.indexer.index_subreddits(self.current_batch)
        self.total_indexed += batch_size
        
        # Update indexer's discovered_ids
        self.indexer.discovered_ids.update(sub['id'] for sub in self.current_batch)
        
        # Clear the batch to free memory
        self.current_batch = []
        
        # Progress feedback
        console.print(f"  [green]✓ Batch {self.batch_count}: Indexed {batch_size} items (Total: {self.total_indexed}/{self.total_collected})[/green]")
    
    def get_stats(self) -> Dict:
        """Get collection statistics"""
        return {
            'total_collected': self.total_collected,
            'total_indexed': self.total_indexed,
            'duplicates_skipped': self.duplicates_skipped,
            'batches_processed': self.batch_count,
            'pending_in_batch': len(self.current_batch),
            'unique_ids_tracked': len(self.seen_ids)
        }

class SubredditIndexer:
    """Main indexer for Reddit subreddits"""
    
    def __init__(self):
        self.reddit = self._init_reddit()
        self.chroma_client = self._init_chromadb()
        self.collection = self._get_or_create_collection()
        self.state = self._load_state()
        self.discovered_ids = self._load_existing_ids()
        self.duplicates_avoided = 0
        
    def _init_reddit(self):
        """Initialize Reddit client"""
        return asyncpraw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "SubredditIndexer/1.0"),
            read_only=True
        )
    
    def _init_chromadb(self):
        """Initialize ChromaDB client"""
        # Use the centralized client factory
        # If running locally and need specific path, can pass custom_path
        return get_chroma_client()
    
    def _get_or_create_collection(self):
        """Get or create ChromaDB collection"""
        return get_collection(COLLECTION_NAME, self.chroma_client)
    
    def _load_state(self) -> Dict:
        """Load indexer state for resume capability"""
        state_path = Path(STATE_FILE)
        if state_path.exists():
            with open(state_path, 'r') as f:
                return json.load(f)
        return {
            "last_full_index": None,
            "last_update": None,
            "indexed_subreddits": [],
            "discovery_progress": {}
        }
    
    def _load_existing_ids(self) -> Set:
        """Load existing subreddit IDs from ChromaDB"""
        try:
            # Get all IDs currently in the collection
            results = self.collection.get(include=[])
            existing_ids = set(results['ids'])
            
            # Also include IDs from state file
            state_ids = set(self.state.get('indexed_subreddits', []))
            
            # Combine both sources
            all_ids = existing_ids.union(state_ids)
            
            if all_ids:
                console.print(f"[green]Loaded {len(all_ids)} existing subreddit IDs[/green]")
            
            return all_ids
        except Exception as e:
            console.print(f"[yellow]Could not load existing IDs: {e}[/yellow]")
            return set()
    
    async def _save_state(self):
        """Save current state"""
        Path(STATE_FILE).parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(STATE_FILE, 'w') as f:
            await f.write(json.dumps(self.state, indent=2))
    
    async def discover_popular_subreddits(self, limit: Optional[int], collector: StreamingDiscoveryCollector):
        """Discover popular subreddits with streaming"""
        console.print("[cyan]Discovering popular subreddits...[/cyan]")
        count = 0
        checked = 0
        
        # Fetch more candidates than needed to account for filtering
        api_limit = (limit * 3) if limit else 5000
        
        try:
            async for subreddit in self.reddit.subreddits.popular(limit=api_limit):
                checked += 1
                if subreddit.id not in collector.seen_ids:
                    data = await self._extract_subreddit_data(subreddit)
                    if data and await self._is_active(subreddit):
                        await collector.add(data)
                        count += 1
                        
                        if count % 100 == 0:
                            console.print(f"  Found {count} popular subreddits...")
                        
                        # Break based on total collected, not just this phase
                        if limit and collector.total_collected >= limit:
                            break
                else:
                    self.duplicates_avoided += 1
                    
                # Also check total collected for early exit
                if limit and collector.total_collected >= limit:
                    break
        except Exception as e:
            console.print(f"[red]Error in popular discovery: {e}[/red]")
        
        console.print(f"  Found {count} popular subreddits")
    
    async def discover_new_subreddits(self, limit: Optional[int], collector: StreamingDiscoveryCollector):
        """Discover newly created subreddits with streaming"""
        console.print("[cyan]Discovering new subreddits...[/cyan]")
        count = 0
        
        # Fetch more candidates than needed to account for filtering
        api_limit = (limit * 3) if limit else 1000
        
        try:
            async for subreddit in self.reddit.subreddits.new(limit=api_limit):
                if subreddit.id not in collector.seen_ids:
                    data = await self._extract_subreddit_data(subreddit)
                    if data and await self._is_active(subreddit):
                        await collector.add(data)
                        count += 1
                        
                        # Break based on total collected, not just this phase
                        if limit and collector.total_collected >= limit:
                            break
                else:
                    self.duplicates_avoided += 1
                    
                # Also check total collected for early exit
                if limit and collector.total_collected >= limit:
                    break
        except Exception as e:
            console.print(f"[red]Error in new discovery: {e}[/red]")
        
        console.print(f"  Found {count} new subreddits")
    
    async def discover_by_search(self, queries: List[str], collector: StreamingDiscoveryCollector, limit_per_query: int = 250):
        """Discover subreddits by search queries with streaming"""
        console.print(f"[cyan]Searching with {len(queries)} queries...[/cyan]")
        total_found = 0
        
        for query in queries:
            try:
                count = 0
                async for subreddit in self.reddit.subreddits.search(query, limit=limit_per_query):
                    if subreddit.id not in collector.seen_ids:
                        data = await self._extract_subreddit_data(subreddit)
                        if data and await self._is_active(subreddit):
                            await collector.add(data)
                            count += 1
                    else:
                        self.duplicates_avoided += 1
                
                if count > 0:
                    console.print(f"  Query '{query}': found {count} subreddits")
                    total_found += count
                    
            except Exception as e:
                console.print(f"[yellow]  Query '{query}' failed: {e}[/yellow]")
                continue
        
        console.print(f"  Total from search: {total_found} subreddits")
    
    async def discover_alphabetical(self, limit: Optional[int], collector: StreamingDiscoveryCollector, comprehensive: bool = False):
        """Discover subreddits alphabetically with streaming"""
        console.print("[cyan]Discovering subreddits alphabetically...[/cyan]")
        
        # Generate search patterns
        import string
        patterns = []
        
        if comprehensive:
            # ALL 2-letter combinations (676 patterns)
            for first in string.ascii_lowercase:
                for second in string.ascii_lowercase:
                    patterns.append(first + second)
            
            # Common 3-letter prefixes (high-yield patterns)
            common_prefixes = ['the', 'new', 'ask', 'get', 'pro', 'all', 'any', 'big', 
                             'hot', 'top', 'old', 'sub', 'not', 'bad', 'fun', 'red',
                             'blu', 'gre', 'bla', 'whi', 'dar', 'lig', 'hig', 'low']
            for prefix in common_prefixes:
                for letter in string.ascii_lowercase[:10]:  # First 10 letters
                    patterns.append(prefix[:2] + letter)
            
            console.print(f"  Generated {len(patterns)} search patterns for comprehensive discovery")
        else:
            # Original limited patterns for faster runs
            patterns.extend(list(string.ascii_lowercase))
            
            # Common two-letter combinations
            for first in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l', 'm', 'n', 'p', 'r', 's', 't']:
                for second in string.ascii_lowercase[:5]:
                    patterns.append(first + second)
            
            # Common prefixes
            patterns.extend(['the', 'my', 'new', 'best', 'true', 'real', 'ask', 'learn'])
        
        # Limit patterns if needed
        if limit and not comprehensive:
            patterns = patterns[:max(10, limit // 100)]
        
        await self.discover_by_search(patterns, collector, limit_per_query=250)
    
    async def discover_by_categories(self, collector: StreamingDiscoveryCollector):
        """Discover subreddits by category searches with streaming"""
        console.print("[cyan]Discovering subreddits by categories...[/cyan]")
        
        categories = [
            # Major topics
            'technology', 'science', 'gaming', 'sports', 'music', 'movies',
            'television', 'books', 'food', 'travel', 'fitness', 'art',
            
            # Interests
            'photography', 'cooking', 'diy', 'crafts', 'gardening', 'pets',
            'fashion', 'beauty', 'cars', 'motorcycles', 'outdoors', 'camping',
            
            # Academic
            'math', 'physics', 'chemistry', 'biology', 'history', 'philosophy',
            'psychology', 'economics', 'politics', 'education', 'language',
            
            # Professional
            'programming', 'business', 'finance', 'investing', 'career', 'jobs',
            'entrepreneur', 'marketing', 'design', 'engineering',
            
            # Lifestyle
            'health', 'mental health', 'relationships', 'parenting', 'advice',
            'selfimprovement', 'meditation', 'minimalism', 'productivity',
            
            # Entertainment
            'anime', 'manga', 'comics', 'games', 'boardgames', 'podcasts',
            'youtube', 'twitch', 'memes', 'funny', 'humor',
            
            # Regional
            'usa', 'europe', 'asia', 'canada', 'australia', 'uk', 'india',
            'news', 'worldnews', 'local'
        ]
        
        await self.discover_by_search(categories, collector, limit_per_query=100)
    
    async def discover_by_smart_search(self, collector: StreamingDiscoveryCollector):
        """Use search_by_name with high-yield prefixes for efficient discovery"""
        console.print("[cyan]Discovering subreddits using smart search patterns...[/cyan]")
        
        # High-yield prefixes based on Reddit naming patterns and English frequency
        smart_prefixes = [
            # High-frequency starts (covers ~60% of subreddits)
            'th', 'he', 'in', 'er', 'an', 're', 'ed', 'on', 'es', 'st',
            'en', 'at', 'to', 'nt', 'ha', 'nd', 'ou', 'ea', 'ng', 'as',
            'or', 'ti', 'wa', 'hi', 'is', 'it', 'te', 'et', 'ar', 'of',
            
            # Reddit-specific common patterns
            'ask', 'new', 'the', 'my', 'bad', 'pro', 'not', 'all', 'get', 'old',
            'true', 'best', 'real', 'shitty', 'casual', 'learn', 'anti', 'ex',
            
            # Important single letters (many subs start with these)
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]
        
        total_found = 0
        for i, prefix in enumerate(smart_prefixes, 1):
            try:
                count = 0
                console.print(f"  Searching '{prefix}' ({i}/{len(smart_prefixes)})...")
                
                # search_by_name can return up to 1000 results per query
                async for subreddit in self.reddit.subreddits.search_by_name(
                    prefix, include_nsfw=True, limit=1000
                ):
                    if subreddit.id not in collector.seen_ids:
                        # Still apply our activity filter
                        if await self._is_active(subreddit):
                            data = await self._extract_subreddit_data(subreddit)
                            if data:
                                await collector.add(data)
                                count += 1
                    else:
                        self.duplicates_avoided += 1
                
                if count > 0:
                    total_found += count
                    console.print(f"    Found {count} active subreddits")
                    
            except Exception as e:
                console.print(f"[yellow]  Error searching '{prefix}': {e}[/yellow]")
                continue
        
        console.print(f"  Total from smart search: {total_found} subreddits")
    
    async def discover_by_recommendation_graph(self, collector: StreamingDiscoveryCollector, max_depth: int = 100):
        """Use Reddit's recommendation engine to discover related subreddits"""
        console.print("[cyan]Discovering subreddits through recommendation graph...[/cyan]")
        
        # Use already discovered subreddits as seeds
        seeds = list(collector.seen_ids)[:100]  # Start with top 100 as seeds
        if not seeds:
            console.print("[yellow]  No seed subreddits available for recommendations[/yellow]")
            return
        
        processed = set()
        to_process = seeds[:20]  # Start with first 20 seeds
        total_found = 0
        
        while to_process and len(processed) < max_depth:
            batch = to_process[:5]  # Process 5 at a time to avoid rate limits
            to_process = to_process[5:]
            
            for seed_id in batch:
                if seed_id in processed:
                    continue
                processed.add(seed_id)
                
                try:
                    # Get the subreddit name from ID (we need the name for recommendations)
                    # First, try to get it from our collected data
                    seed_name = None
                    try:
                        # Get subreddit by ID to get its name
                        result = self.collection.get(ids=[seed_id], include=['metadata'])
                        if result and result['metadatas'] and result['metadatas'][0]:
                            seed_name = result['metadatas'][0].get('name')
                    except:
                        pass
                    
                    if not seed_name:
                        continue
                    
                    # Get Reddit's recommendations for this subreddit
                    count = 0
                    async for recommended in self.reddit.subreddits.recommended(
                        subreddits=[seed_name], omit_subreddits=list(collector.seen_ids)[:100]
                    ):
                        if recommended.id not in collector.seen_ids:
                            if await self._is_active(recommended):
                                data = await self._extract_subreddit_data(recommended)
                                if data:
                                    await collector.add(data)
                                    count += 1
                                    total_found += 1
                                    
                                    # Add to processing queue for recursive discovery
                                    if len(processed) < max_depth and recommended.id not in processed:
                                        to_process.append(recommended.id)
                        else:
                            self.duplicates_avoided += 1
                    
                    if count > 0:
                        console.print(f"  Seed '{seed_name}': found {count} related subreddits")
                        
                except Exception as e:
                    # Silently skip errors for individual seeds
                    continue
        
        console.print(f"  Total from recommendation graph: {total_found} subreddits")
    
    async def discover_default_and_gold(self, collector: StreamingDiscoveryCollector):
        """Discover default and gold (premium) subreddits"""
        console.print("[cyan]Discovering default and premium subreddits...[/cyan]")
        
        total_found = 0
        
        # Get default subreddits
        try:
            count = 0
            async for subreddit in self.reddit.subreddits.default(limit=None):
                if subreddit.id not in collector.seen_ids:
                    data = await self._extract_subreddit_data(subreddit)
                    if data:
                        await collector.add(data)
                        count += 1
                else:
                    self.duplicates_avoided += 1
            
            if count > 0:
                console.print(f"  Found {count} default subreddits")
                total_found += count
        except Exception as e:
            console.print(f"[yellow]  Error getting default subreddits: {e}[/yellow]")
        
        # Get gold/premium subreddits
        try:
            count = 0
            async for subreddit in self.reddit.subreddits.gold():
                if subreddit.id not in collector.seen_ids:
                    data = await self._extract_subreddit_data(subreddit)
                    if data:
                        await collector.add(data)
                        count += 1
                else:
                    self.duplicates_avoided += 1
            
            if count > 0:
                console.print(f"  Found {count} premium subreddits")
                total_found += count
        except Exception as e:
            console.print(f"[yellow]  Error getting premium subreddits: {e}[/yellow]")
        
        console.print(f"  Total from default/premium: {total_found} subreddits")
    
    async def discover_by_topic_search(self, collector: StreamingDiscoveryCollector):
        """Use search_by_topic for topical discovery"""
        console.print("[cyan]Discovering subreddits by topic search...[/cyan]")
        
        # Major topics to search
        topics = [
            'technology', 'gaming', 'sports', 'politics', 'science',
            'entertainment', 'music', 'movies', 'television', 'books',
            'food', 'travel', 'fitness', 'health', 'education',
            'business', 'finance', 'cryptocurrency', 'programming', 'art',
            'photography', 'nature', 'animals', 'history', 'philosophy',
            'psychology', 'relationships', 'parenting', 'fashion', 'beauty'
        ]
        
        total_found = 0
        for topic in topics:
            try:
                count = 0
                async for subreddit in self.reddit.subreddits.search_by_topic(topic):
                    if subreddit.id not in collector.seen_ids:
                        if await self._is_active(subreddit):
                            data = await self._extract_subreddit_data(subreddit)
                            if data:
                                await collector.add(data)
                                count += 1
                    else:
                        self.duplicates_avoided += 1
                
                if count > 0:
                    console.print(f"  Topic '{topic}': found {count} subreddits")
                    total_found += count
                    
            except Exception as e:
                console.print(f"[yellow]  Topic '{topic}' failed: {e}[/yellow]")
                continue
        
        console.print(f"  Total from topic search: {total_found} subreddits")
    
    async def discover_by_common_words(self, collector: StreamingDiscoveryCollector):
        """Discover subreddits using common words and terms"""
        console.print("[cyan]Discovering subreddits by common words...[/cyan]")
        
        # Common words that often appear in subreddit names
        common_words = [
            # Top English words
            'world', 'life', 'people', 'history', 'today', 'tomorrow', 'future',
            'love', 'hate', 'happy', 'sad', 'angry', 'funny', 'serious',
            
            # Activities
            'watch', 'read', 'write', 'play', 'work', 'study', 'learn', 'teach',
            'build', 'create', 'make', 'design', 'code', 'program', 'develop',
            
            # Hobbies
            'hobby', 'craft', 'collect', 'trade', 'share', 'show', 'discuss',
            
            # Time-related
            'daily', 'weekly', 'monthly', 'yearly', '2020', '2021', '2022', '2023', '2024',
            
            # Numbers
            '101', '420', '69', '100', '1000', 'first', 'second', 'one', 'two',
            
            # Locations
            'america', 'europe', 'asia', 'africa', 'australia', 'city', 'country',
            'state', 'nation', 'global', 'international', 'local',
            
            # Adjectives
            'good', 'bad', 'better', 'best', 'worst', 'great', 'terrible',
            'amazing', 'awesome', 'cool', 'hot', 'cold', 'old', 'young',
            
            # Tech terms
            'tech', 'digital', 'online', 'internet', 'web', 'app', 'software',
            'hardware', 'data', 'crypto', 'bitcoin', 'nft', 'meta', 'virtual',
            
            # Social
            'social', 'community', 'group', 'team', 'club', 'society', 'network',
            
            # Question words
            'what', 'why', 'how', 'when', 'where', 'who', 'which',
            
            # Specific interests
            'anime', 'manga', 'comic', 'movie', 'film', 'tv', 'series', 'show',
            'game', 'gaming', 'gamer', 'pc', 'console', 'mobile',
            'food', 'recipe', 'cooking', 'baking', 'eating',
            'travel', 'trip', 'tour', 'visit', 'explore',
            'photo', 'picture', 'image', 'video', 'gif', 'meme',
            'music', 'song', 'band', 'artist', 'album',
            'book', 'novel', 'story', 'writing', 'author',
            'sport', 'team', 'player', 'league', 'match',
            'car', 'bike', 'vehicle', 'drive', 'ride',
            'pet', 'dog', 'cat', 'animal', 'bird', 'fish',
            'plant', 'garden', 'tree', 'flower', 'nature'
        ]
        
        await self.discover_by_search(common_words, collector, limit_per_query=250)
    
    async def _is_active(self, subreddit) -> bool:
        """Check if subreddit is active"""
        try:
            # Check basic accessibility
            if subreddit.subreddit_type == 'private':
                return False
            
            # Check subscriber threshold
            if subreddit.subscribers < MIN_SUBSCRIBERS:
                return False
            
            # Check for recent posts
            recent_posts = []
            async for post in subreddit.new(limit=3):
                recent_posts.append(post)
            
            if not recent_posts:
                return False
            
            # Check if most recent post is within threshold
            latest_post_age = time.time() - recent_posts[0].created_utc
            days_old = latest_post_age / (24 * 3600)
            
            return days_old <= ACTIVITY_THRESHOLD_DAYS
            
        except Exception:
            return False
    
    async def _extract_subreddit_data(self, subreddit) -> Optional[Dict]:
        """Extract data from subreddit for indexing"""
        try:
            return {
                'id': subreddit.id,
                'name': subreddit.display_name,
                'title': subreddit.title or subreddit.display_name,
                'description': subreddit.public_description or "",
                'sidebar': (subreddit.description or "")[:2000],  # Truncate long sidebars
                'subscribers': subreddit.subscribers or 0,
                'created_utc': subreddit.created_utc,
                'over18': subreddit.over18,
                'url': f"https://reddit.com/r/{subreddit.display_name}",
                'indexed_at': datetime.now().isoformat()
            }
        except Exception as e:
            return None
    
    def _create_embedding_text(self, data: Dict) -> str:
        """Create text for embedding"""
        return f"""
        Subreddit: r/{data['name']}
        Title: {data['title']}
        Description: {data['description']}
        
        Community info: {data['sidebar'][:500]}
        
        Size: {data['subscribers']} members
        """
    
    async def index_subreddits(self, subreddits: List[Dict]):
        """Index subreddits in ChromaDB"""
        if not subreddits:
            return
        
        console.print(f"[green]Indexing {len(subreddits)} subreddits...[/green]")
        
        documents = []
        metadatas = []
        ids = []
        
        for sub in subreddits:
            # Create embedding text
            doc_text = self._create_embedding_text(sub)
            
            # Prepare metadata
            metadata = {
                'name': sub['name'],
                'subscribers': sub['subscribers'],
                'nsfw': sub['over18'],
                'created': sub['created_utc'],
                'indexed_at': sub['indexed_at'],
                'url': sub['url']
            }
            
            documents.append(doc_text)
            metadatas.append(metadata)
            ids.append(sub['id'])
        
        # Index in batches
        for i in range(0, len(documents), BATCH_SIZE):
            batch_end = min(i + BATCH_SIZE, len(documents))
            
            try:
                self.collection.upsert(
                    documents=documents[i:batch_end],
                    metadatas=metadatas[i:batch_end],
                    ids=ids[i:batch_end]
                )
            except Exception as e:
                console.print(f"[red]Error indexing batch: {e}[/red]")
    
    async def build_full_index(self, limit: Optional[int] = None, comprehensive: bool = False):
        """Build complete index from scratch using streaming approach"""
        mode = "COMPREHENSIVE" if comprehensive else "standard"
        console.print(f"[bold green]Building {mode} subreddit index (streaming mode)...[/bold green]")
        start_time = time.time()
        
        # Initialize streaming collector
        batch_size = 500 if comprehensive else 250
        collector = StreamingDiscoveryCollector(self, batch_size=batch_size)
        
        # Adjust limits for comprehensive mode
        popular_limit = 10000 if comprehensive else (limit or 5000)
        new_limit = 5000 if comprehensive else (limit or 1000)
        
        # Discovery phases with streaming
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            
            # Phase 1: Default and Premium subreddits (quick win)
            task = progress.add_task("[cyan]Default and premium subreddits...", total=None)
            await self.discover_default_and_gold(collector=collector)
            progress.update(task, completed=100)
            
            # Phase 2: Popular subreddits
            if not limit or collector.total_collected < limit:
                task = progress.add_task(f"[cyan]Popular subreddits (up to {popular_limit})...", total=None)
                await self.discover_popular_subreddits(
                    limit,  # Pass the user's limit, discovery method will handle it
                    collector=collector
                )
                progress.update(task, completed=100)
            
            # Phase 3: Smart search with high-yield prefixes
            if not limit or collector.total_collected < limit:
                task = progress.add_task("[cyan]Smart prefix search...", total=None)
                await self.discover_by_smart_search(collector=collector)
                progress.update(task, completed=100)
            
            # Phase 4: Topic-based discovery
            if not limit or collector.total_collected < limit:
                task = progress.add_task("[cyan]Topic-based search...", total=None)
                await self.discover_by_topic_search(collector=collector)
                progress.update(task, completed=100)
            
            # Phase 5: New subreddits
            if not limit or collector.total_collected < limit:
                task = progress.add_task(f"[cyan]New subreddits (up to {new_limit})...", total=None)
                await self.discover_new_subreddits(
                    limit,  # Pass the same limit, method will check collector.total_collected
                    collector=collector
                )
                progress.update(task, completed=100)
            
            # Phase 6: Recommendation graph (finds hidden gems)
            if not limit or collector.total_collected < limit:
                task = progress.add_task("[cyan]Recommendation graph traversal...", total=None)
                await self.discover_by_recommendation_graph(collector=collector)
                progress.update(task, completed=100)
            
            # Phase 7: Category search
            if not limit or collector.total_collected < limit:
                task = progress.add_task("[cyan]Category search...", total=None)
                await self.discover_by_categories(collector=collector)
                progress.update(task, completed=100)
            
            # Phase 8: Alphabetical search (if still need more)
            if comprehensive and (not limit or collector.total_collected < limit):
                task = progress.add_task("[cyan]Alphabetical search...", total=None)
                await self.discover_alphabetical(
                    limit if limit else None,
                    collector=collector,
                    comprehensive=comprehensive
                )
                progress.update(task, completed=100)
            
            # Phase 9: Word-based discovery (comprehensive mode only)
            if comprehensive and (not limit or collector.total_collected < limit):
                task = progress.add_task("[cyan]Word-based discovery...", total=None)
                await self.discover_by_common_words(collector=collector)
                progress.update(task, completed=100)
        
        # Final flush of any remaining items
        await collector.flush()
        
        # Update state
        self.state['last_full_index'] = datetime.now().isoformat()
        self.state['indexed_subreddits'] = list(collector.seen_ids)
        await self._save_state()
        
        # Report results
        stats = collector.get_stats()
        elapsed = time.time() - start_time
        
        console.print(f"\n[bold green]✅ Indexing complete (Streaming Mode)![/bold green]")
        console.print(f"  Total discovered: {stats['total_collected']}")
        console.print(f"  Total indexed: {stats['total_indexed']}")
        console.print(f"  Duplicates avoided: {stats['duplicates_skipped'] + self.duplicates_avoided}")
        console.print(f"  Batches processed: {stats['batches_processed']}")
        console.print(f"  Time elapsed: {elapsed:.1f} seconds")
        console.print(f"  Index location: ChromaDB Cloud")
        console.print(f"  Memory efficient: ✓ (Max ~{batch_size * 2}KB in memory)")
    
    async def update_index(self):
        """Incremental update of existing index"""
        console.print("[bold yellow]Updating subreddit index...[/bold yellow]")
        
        # Use streaming collector for updates too
        collector = StreamingDiscoveryCollector(self, batch_size=250)
        
        # Discover new subreddits
        await self.discover_new_subreddits(limit=500, collector=collector)
        
        # Re-check popular for changes
        await self.discover_popular_subreddits(limit=1000, collector=collector)
        
        # Final flush
        await collector.flush()
        
        stats = collector.get_stats()
        if stats['total_indexed'] > 0:
            console.print(f"[green]Added {stats['total_indexed']} new subreddits[/green]")
        else:
            console.print("[yellow]No new subreddits found[/yellow]")
        
        # Update state
        self.state['last_update'] = datetime.now().isoformat()
        self.state['indexed_subreddits'] = list(collector.seen_ids)
        await self._save_state()
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        stats = {
            'total_indexed': self.collection.count(),
            'last_full_index': self.state.get('last_full_index', 'Never'),
            'last_update': self.state.get('last_update', 'Never'),
            'duplicates_avoided': self.duplicates_avoided,
            'collection_name': COLLECTION_NAME,
            'location': 'ChromaDB Cloud',
            'min_subscribers': MIN_SUBSCRIBERS
        }
        return stats
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.reddit.close()

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Reddit Subreddit ChromaDB Indexer')
    parser.add_argument('--build', action='store_true', help='Build full index')
    parser.add_argument('--update', action='store_true', help='Update existing index')
    parser.add_argument('--status', action='store_true', help='Show index status')
    parser.add_argument('--limit', type=int, help='Limit number of subreddits (for testing)')
    parser.add_argument('--comprehensive', action='store_true', 
                       help='Use comprehensive discovery (finds 30,000+ subreddits, takes 8-12 hours)')
    
    args = parser.parse_args()
    
    # Check environment
    if not os.getenv("REDDIT_CLIENT_ID") or not os.getenv("REDDIT_CLIENT_SECRET"):
        console.print("[red]Error: Reddit API credentials not found in environment[/red]")
        console.print("Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET")
        return
    
    indexer = SubredditIndexer()
    
    try:
        if args.build:
            await indexer.build_full_index(limit=args.limit, comprehensive=args.comprehensive)
        elif args.update:
            await indexer.update_index()
        elif args.status:
            stats = indexer.get_stats()
            
            # Display stats in table
            table = Table(title="Subreddit Index Status")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="magenta")
            
            table.add_row("Total Indexed", f"{stats['total_indexed']:,}")
            table.add_row("Min Subscribers", f"{stats['min_subscribers']:,}")
            table.add_row("Last Full Index", stats['last_full_index'])
            table.add_row("Last Update", stats['last_update'])
            table.add_row("Collection", stats['collection_name'])
            table.add_row("Location", stats['location'])
            
            console.print(table)
        else:
            console.print("Use --build, --update, or --status")
            console.print("Run with --help for more options")
    
    finally:
        await indexer.cleanup()

if __name__ == "__main__":
    asyncio.run(main())