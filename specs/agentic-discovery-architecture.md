# Agentic Discovery Architecture with OpenAI Agents SDK

## Overview
This document outlines the refactoring of the monolithic `discover.py` tool into a modular, agentic architecture using OpenAI's Python Agents SDK. Each agent has a single, well-defined responsibility and can hand off to other specialized agents as needed.

### Why Agentic Architecture?

The current monolithic `discover.py` file (400+ lines) combines multiple concerns:
- Query processing and analysis
- API interaction and error handling
- Scoring and ranking algorithms
- Result formatting and synthesis
- Batch operations management

This creates several problems:
1. **Testing Complexity**: Can't test scoring without API calls
2. **Limited Reusability**: Can't use validation logic elsewhere
3. **Performance Issues**: Sequential processing of batch requests
4. **Maintenance Burden**: Changes risk breaking unrelated functionality
5. **Scaling Challenges**: Adding features requires modifying core logic

The agentic approach solves these issues by decomposing functionality into specialized, autonomous agents that collaborate through well-defined interfaces.

## Architecture Principles

1. **Single Responsibility**: Each agent performs one specific task excellently
2. **Composability**: Agents can be combined in different ways for various workflows
3. **Testability**: Each agent can be tested in isolation
4. **Observability**: Full tracing of agent decision-making process
5. **Efficiency**: Smart routing and parallel execution where possible

## Directory Structure

```
reddit-research-mcp/src/
├── agents/
│   ├── __init__.py
│   ├── discovery_orchestrator.py
│   ├── query_analyzer.py
│   ├── subreddit_scorer.py
│   ├── search_executor.py
│   ├── batch_manager.py
│   ├── validator.py
│   └── synthesizer.py
├── models/
│   ├── __init__.py
│   ├── discovery_context.py
│   └── discovery_models.py
├── tools/
│   └── discover_agent.py
```

## Agent Specifications

### 1. Discovery Orchestrator Agent
**File**: `agents/discovery_orchestrator.py`

**Purpose**: Routes discovery requests to the appropriate specialized agent based on query type and requirements.

**Why This Agent?**
The Discovery Orchestrator serves as the intelligent entry point that prevents inefficient processing. In the monolithic approach, every query goes through the same pipeline regardless of complexity. This agent enables:
- **Smart Routing**: Simple queries skip unnecessary analysis steps
- **Resource Optimization**: Uses appropriate agents based on query complexity
- **Error Isolation**: Failures in one path don't affect others
- **Scalability**: New discovery strategies can be added without modifying core logic

**Architectural Role**:
- **Entry Point**: First agent in every discovery workflow
- **Traffic Director**: Routes to specialized agents based on intent
- **Fallback Handler**: Manages errors and edge cases gracefully
- **Performance Optimizer**: Chooses fastest path for each query type

**Problem Solved**: 
The monolithic `discover.py` processes all queries identically, wasting resources on simple validations and lacking optimization for batch operations. The orchestrator eliminates this inefficiency.

**Key Interactions**:
- **Receives**: Raw discovery requests from the main entry point
- **Delegates To**: Query Analyzer (complex), Batch Manager (multiple), Validator (verification), Search Executor (simple)
- **Returns**: Final results from delegated agents

**Key Responsibilities**:
- Analyze incoming discovery requests
- Determine optimal discovery strategy
- Route to appropriate specialized agent
- Handle edge cases and errors gracefully

**Model**: `gpt-4o-mini` (lightweight routing decisions)

**Handoffs**:
- Query Analyzer (for complex queries)
- Batch Manager (for multiple queries)
- Validator (for direct validation)
- Search Executor (for simple searches)

**Implementation**:
```python
from agents import Agent, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

discovery_orchestrator = Agent[DiscoveryContext](
    name="Discovery Orchestrator",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a routing agent for Reddit discovery requests.
    
    Analyze the incoming request and determine the best path:
    - Complex queries needing analysis → Query Analyzer
    - Batch/multiple queries → Batch Manager  
    - Direct subreddit validation → Validator
    - Simple searches → Search Executor
    
    Consider efficiency and accuracy when routing.
    """,
    model="gpt-4o-mini",
    handoffs=[query_analyzer, batch_manager, validator, search_executor]
)
```

### 2. Query Analyzer Agent
**File**: `agents/query_analyzer.py`

**Purpose**: Analyzes and enhances search queries for better results.

**Why This Agent?**
Reddit's search API is notoriously limited and literal. The Query Analyzer transforms vague or complex user queries into optimized search strategies. This agent provides:
- **Semantic Understanding**: Interprets user intent beyond literal keywords
- **Query Expansion**: Adds synonyms and related terms for comprehensive results
- **Search Strategy**: Determines best approach (broad vs. specific search)
- **Intent Classification**: Distinguishes between topic exploration vs. specific community search

**Architectural Role**:
- **Query Preprocessor**: Enhances queries before they hit the Reddit API
- **Intent Detector**: Classifies what the user is really looking for
- **Strategy Advisor**: Recommends search approaches to downstream agents
- **NLP Specialist**: Applies language understanding to improve results

**Problem Solved**:
The monolithic approach uses raw queries directly, leading to poor results when users use natural language or ambiguous terms. This agent bridges the gap between human expression and API requirements.

**Key Interactions**:
- **Receives From**: Discovery Orchestrator (complex queries)
- **Processes**: Raw user queries into structured search plans
- **Hands Off To**: Search Executor (with enhanced query and strategy)
- **Provides**: Keywords, expanded terms, and intent classification

**Key Responsibilities**:
- Extract keywords and intent
- Expand query with related terms
- Classify query type (topic, community, specific)
- Generate search strategies

**Tools**:
```python
@function_tool
def extract_keywords(wrapper: RunContextWrapper[DiscoveryContext], text: str) -> List[str]:
    """Extract meaningful keywords from query text."""
    # Implementation from current discover.py
    
@function_tool
def expand_query(wrapper: RunContextWrapper[DiscoveryContext], query: str) -> QueryExpansion:
    """Expand query with synonyms and related terms."""
    # Generate variations and related terms
    
@function_tool
def classify_intent(wrapper: RunContextWrapper[DiscoveryContext], query: str) -> QueryIntent:
    """Classify the intent behind the query."""
    # Return: topic_search, community_search, validation, etc.
```

**Output Type**:
```python
class AnalyzedQuery(BaseModel):
    original: str
    keywords: List[str]
    expanded_terms: List[str]
    intent: QueryIntent
    suggested_strategy: str
    confidence: float
```

**Model**: `gpt-4o` (complex language understanding)

**Handoffs**: Search Executor (with enhanced query)

### 3. Subreddit Scorer Agent
**File**: `agents/subreddit_scorer.py`

**Purpose**: Scores and ranks subreddit relevance with detailed confidence metrics.

**Why This Agent?**
Reddit's search API returns results in arbitrary order with many false positives. The Subreddit Scorer applies sophisticated ranking algorithms to surface the most relevant communities. This agent provides:
- **Multi-Factor Scoring**: Combines name match, description relevance, and activity levels
- **False Positive Detection**: Identifies and penalizes misleading matches
- **Confidence Metrics**: Provides transparency about why results are ranked
- **Activity Weighting**: Prioritizes active communities over dead ones

**Architectural Role**:
- **Quality Filter**: Ensures only relevant results reach the user
- **Ranking Engine**: Orders results by true relevance, not API defaults
- **Confidence Calculator**: Provides scoring transparency
- **Post-Processor**: Refines raw search results into useful recommendations

**Problem Solved**:
The monolithic approach has scoring logic embedded throughout, making it hard to tune or test. False positives (like "pythonball" for "python") pollute results. This agent centralizes and perfects scoring logic.

**Key Interactions**:
- **Receives From**: Search Executor (raw search results)
- **Processes**: Unranked subreddits into scored, ranked list
- **Sends To**: Result Synthesizer (for final formatting)
- **Collaborates With**: Batch Manager (for scoring multiple search results)

**Key Responsibilities**:
- Calculate name match scores
- Evaluate description relevance
- Assess community activity
- Apply penalties for false positives
- Generate confidence scores

**Tools**:
```python
@function_tool
def calculate_name_match(wrapper: RunContextWrapper[DiscoveryContext], 
                         subreddit_name: str, query: str) -> float:
    """Calculate how well subreddit name matches query."""
    # Implementation from current discover.py
    
@function_tool
def calculate_description_score(wrapper: RunContextWrapper[DiscoveryContext],
                               description: str, query: str) -> float:
    """Score based on query presence in description."""
    # Implementation from current discover.py
    
@function_tool
def calculate_activity_score(wrapper: RunContextWrapper[DiscoveryContext],
                            subscribers: int) -> float:
    """Score based on community size and activity."""
    # Implementation from current discover.py
    
@function_tool
def calculate_penalties(wrapper: RunContextWrapper[DiscoveryContext],
                       subreddit_name: str, query: str) -> float:
    """Apply penalties for likely false positives."""
    # Implementation from current discover.py
```

**Output Type**:
```python
class ScoredSubreddit(BaseModel):
    name: str
    confidence: float
    match_type: str
    score_breakdown: Dict[str, float]
    ranking: int
```

**Model**: `gpt-4o-mini` (mathematical calculations)

**Tool Use Behavior**: `stop_on_first_tool` (direct scoring results)

### 4. Search Executor Agent
**File**: `agents/search_executor.py`

**Purpose**: Executes Reddit API searches efficiently with error handling.

**Why This Agent?**
Direct API interaction requires careful error handling, rate limit management, and caching. The Search Executor isolates all Reddit API complexity from other agents. This agent provides:
- **API Abstraction**: Other agents don't need to know Reddit API details
- **Error Resilience**: Handles rate limits, timeouts, and API failures gracefully
- **Caching Layer**: Prevents redundant API calls for identical queries
- **Result Validation**: Ensures data integrity before passing downstream

**Architectural Role**:
- **API Gateway**: Single point of contact with Reddit API
- **Error Handler**: Manages all API-related failures and retries
- **Cache Manager**: Stores and retrieves recent search results
- **Data Validator**: Ensures results are complete and valid

**Problem Solved**:
The monolithic approach mixes API calls with business logic, making it hard to handle errors consistently or implement caching. This agent centralizes all API interaction concerns.

**Key Interactions**:
- **Receives From**: Query Analyzer (enhanced queries) or Orchestrator (simple queries)
- **Interacts With**: Reddit API via PRAW client
- **Sends To**: Subreddit Scorer (for ranking)
- **Caches**: Results in context for reuse by other agents

**Key Responsibilities**:
- Execute Reddit API search calls
- Handle API errors and rate limits
- Validate returned results
- Cache results for efficiency

**Tools**:
```python
@function_tool
async def search_reddit(wrapper: RunContextWrapper[DiscoveryContext],
                        query: str, limit: int = 250) -> List[RawSubreddit]:
    """Execute Reddit search API call."""
    reddit = wrapper.context.reddit_client
    results = []
    for subreddit in reddit.subreddits.search(query, limit=limit):
        results.append(RawSubreddit.from_praw(subreddit))
    return results
    
@function_tool
def handle_api_error(wrapper: RunContextWrapper[DiscoveryContext],
                     error: Exception) -> ErrorStrategy:
    """Determine how to handle API errors."""
    # Retry logic, fallback strategies, etc.
```

**Output Type**:
```python
class SearchResults(BaseModel):
    query: str
    results: List[RawSubreddit]
    total_found: int
    api_calls: int
    cached: bool
    errors: List[str]
```

**Model**: `gpt-4o-mini` (simple execution)

**Handoffs**: Subreddit Scorer (for ranking results)

### 5. Batch Discovery Manager Agent
**File**: `agents/batch_manager.py`

**Purpose**: Manages batch discovery operations for multiple queries.

**Why This Agent?**
Users often need to discover communities across multiple related topics. The Batch Manager orchestrates parallel searches efficiently. This agent provides:
- **Parallel Execution**: Runs multiple searches concurrently for speed
- **Deduplication**: Removes duplicate subreddits across different searches
- **API Optimization**: Minimizes total API calls through smart batching
- **Result Aggregation**: Combines multiple search results intelligently

**Architectural Role**:
- **Parallel Coordinator**: Manages multiple Search Executor instances
- **Resource Manager**: Optimizes API usage across batch operations
- **Result Aggregator**: Merges and deduplicates results from multiple searches
- **Performance Optimizer**: Ensures batch operations complete quickly

**Problem Solved**:
The monolithic approach processes batch queries sequentially, leading to slow performance. It also lacks sophisticated deduplication and aggregation logic for multiple searches.

**Key Interactions**:
- **Receives From**: Discovery Orchestrator (batch requests)
- **Spawns**: Multiple Search Executor agents in parallel
- **Coordinates**: Parallel execution and result collection
- **Sends To**: Result Synthesizer (aggregated results)

**Key Responsibilities**:
- Coordinate multiple search operations
- Optimize API calls through batching
- Aggregate results from multiple searches
- Manage parallel execution

**Tools**:
```python
@function_tool
async def coordinate_batch(wrapper: RunContextWrapper[DiscoveryContext],
                          queries: List[str]) -> BatchPlan:
    """Plan optimal batch execution strategy."""
    # Determine parallelization, caching opportunities
    
@function_tool
def merge_batch_results(wrapper: RunContextWrapper[DiscoveryContext],
                        results: List[SearchResults]) -> BatchResults:
    """Merge results from multiple searches."""
    # Deduplicate, aggregate, summarize
```

**Model**: `gpt-4o` (complex coordination)

**Handoffs**: Multiple Search Executor agents (in parallel)

**Implementation Note**: Uses dynamic handoff creation for parallel execution

### 6. Subreddit Validator Agent
**File**: `agents/validator.py`

**Purpose**: Validates subreddit existence and accessibility.

**Why This Agent?**
Users often have specific subreddit names that need verification. The Validator provides quick, focused validation without the overhead of full search. This agent provides:
- **Direct Validation**: Checks specific subreddit names efficiently
- **Access Verification**: Confirms subreddits are public and accessible
- **Alternative Suggestions**: Recommends similar communities if validation fails
- **Metadata Retrieval**: Gets detailed info about valid subreddits

**Architectural Role**:
- **Verification Specialist**: Focused solely on validation tasks
- **Fast Path**: Provides quick responses for known subreddit names
- **Fallback Provider**: Suggests alternatives when validation fails
- **Metadata Fetcher**: Retrieves comprehensive subreddit information

**Problem Solved**:
The monolithic approach treats validation as a special case of search, which is inefficient. Users waiting to verify "r/python" shouldn't trigger a full search pipeline.

**Key Interactions**:
- **Receives From**: Discovery Orchestrator (direct validation requests)
- **Validates**: Specific subreddit names via Reddit API
- **Returns**: Validation status with metadata or alternatives
- **May Trigger**: Search Executor (to find alternatives if validation fails)

**Key Responsibilities**:
- Check if subreddit exists
- Verify accessibility (not private/banned)
- Get detailed subreddit information
- Suggest alternatives if invalid

**Tools**:
```python
@function_tool
def validate_subreddit(wrapper: RunContextWrapper[DiscoveryContext],
                       subreddit_name: str) -> ValidationResult:
    """Validate if subreddit exists and is accessible."""
    # Implementation from current discover.py
    
@function_tool
def get_subreddit_info(wrapper: RunContextWrapper[DiscoveryContext],
                       subreddit_name: str) -> SubredditInfo:
    """Get detailed information about a subreddit."""
    # Fetch all metadata
```

**Output Type**:
```python
class ValidationResult(BaseModel):
    valid: bool
    name: str
    reason: Optional[str]
    info: Optional[SubredditInfo]
    suggestions: List[str]
```

**Model**: `gpt-4o-mini` (simple validation)

### 7. Result Synthesizer Agent
**File**: `agents/synthesizer.py`

**Purpose**: Synthesizes and formats final discovery results.

**Why This Agent?**
Raw scored results need intelligent synthesis to be truly useful. The Result Synthesizer transforms data into actionable insights. This agent provides:
- **Intelligent Summarization**: Creates meaningful summaries from result patterns
- **Actionable Recommendations**: Suggests next steps based on results
- **Flexible Formatting**: Adapts output format to use case
- **Insight Generation**: Identifies patterns and relationships in results

**Architectural Role**:
- **Final Processor**: Last agent before results return to user
- **Insight Generator**: Transforms data into understanding
- **Format Adapter**: Ensures results match expected output format
- **Recommendation Engine**: Provides actionable next steps

**Problem Solved**:
The monolithic approach mixes result formatting throughout the code, making it hard to maintain consistent output or add new insights. This agent centralizes all presentation logic.

**Key Interactions**:
- **Receives From**: Subreddit Scorer or Batch Manager (scored/aggregated results)
- **Synthesizes**: Raw data into formatted, insightful output
- **Generates**: Summaries, recommendations, and metadata
- **Returns**: Final formatted results to the orchestrator

**Key Responsibilities**:
- Format results for presentation
- Generate summaries and insights
- Create recommendations
- Add metadata and next actions

**Tools**:
```python
@function_tool
def format_results(wrapper: RunContextWrapper[DiscoveryContext],
                  results: List[ScoredSubreddit]) -> FormattedResults:
    """Format results for final output."""
    # Structure for easy consumption
    
@function_tool
def generate_recommendations(wrapper: RunContextWrapper[DiscoveryContext],
                            results: FormattedResults) -> List[str]:
    """Generate actionable recommendations."""
    # Next steps, additional searches, etc.
```

**Output Type**:
```python
class DiscoveryOutput(BaseModel):
    results: List[FormattedSubreddit]
    summary: DiscoverySummary
    recommendations: List[str]
    metadata: DiscoveryMetadata
```

**Model**: `gpt-4o` (synthesis and insights)

## Agent Collaboration Workflow

### Example: Complex Query Discovery

When a user searches for "machine learning communities for beginners":

1. **Discovery Orchestrator** receives request, identifies complexity, routes to Query Analyzer
2. **Query Analyzer** extracts keywords ["machine learning", "beginners", "ML", "learn"], expands query, identifies intent as "topic_search"
3. **Search Executor** runs enhanced searches for each term variation
4. **Subreddit Scorer** ranks results, penalizing advanced communities, boosting beginner-friendly ones
5. **Result Synthesizer** formats top results with recommendations for getting started

### Example: Batch Validation

When validating multiple subreddit names ["r/python", "r/datascience", "r/doesnotexist"]:

1. **Discovery Orchestrator** identifies validation request, routes to Batch Manager
2. **Batch Manager** spawns three parallel Validator agents
3. **Validators** check each subreddit simultaneously
4. **Result Synthesizer** aggregates validation results, suggests alternatives for invalid entries

## Shared Models and Context

### Discovery Context
**File**: `models/discovery_context.py`

```python
from dataclasses import dataclass
import praw
from typing import Dict, Any, Optional

@dataclass
class DiscoveryContext:
    reddit_client: praw.Reddit
    query_metadata: Optional[QueryMetadata] = None
    discovery_config: DiscoveryConfig = field(default_factory=DiscoveryConfig)
    api_call_counter: int = 0
    cache: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class QueryMetadata:
    original_query: str
    intent: str
    timestamp: float
    user_preferences: Dict[str, Any]
    
@dataclass
class DiscoveryConfig:
    include_nsfw: bool = False
    max_api_calls: int = 10
    cache_ttl: int = 300
    default_limit: int = 10
```

### Discovery Models
**File**: `models/discovery_models.py`

```python
from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

class QueryIntent(BaseModel):
    type: Literal["topic_search", "community_search", "validation", "batch"]
    confidence: float
    
class RawSubreddit(BaseModel):
    name: str
    title: str
    description: str
    subscribers: int
    over_18: bool
    created_utc: float
    url: str
    
    @classmethod
    def from_praw(cls, subreddit):
        """Create from PRAW subreddit object."""
        return cls(
            name=subreddit.display_name,
            title=subreddit.title,
            description=subreddit.public_description[:100],
            subscribers=subreddit.subscribers,
            over_18=subreddit.over18,
            created_utc=subreddit.created_utc,
            url=f"https://reddit.com/r/{subreddit.display_name}"
        )

class ConfidenceScore(BaseModel):
    overall: float
    name_match: float
    description_match: float
    activity_score: float
    penalties: float
    
class DiscoverySummary(BaseModel):
    total_found: int
    returned: int
    coverage: Literal["comprehensive", "good", "partial", "limited"]
    top_by_confidence: List[str]
    confidence_distribution: Dict[str, int]
```

## Main Entry Point

### Discover Agent Tool
**File**: `tools/discover_agent.py`

```python
from agents import Agent, Runner
from src.models.discovery_context import DiscoveryContext
from src.agents import discovery_orchestrator
import praw

async def discover_subreddits_agent(
    query: Optional[str] = None,
    queries: Optional[List[str]] = None,
    reddit: praw.Reddit = None,
    limit: int = 10,
    include_nsfw: bool = False
) -> DiscoveryOutput:
    """
    Agentic version of discover_subreddits using OpenAI Agents SDK.
    
    Maintains backward compatibility with existing interface.
    """
    # Initialize context
    context = DiscoveryContext(
        reddit_client=reddit,
        discovery_config=DiscoveryConfig(
            include_nsfw=include_nsfw,
            default_limit=limit
        )
    )
    
    # Prepare input
    if queries:
        input_text = f"Batch discovery for queries: {queries}"
    else:
        input_text = f"Discover subreddits for: {query}"
    
    # Run discovery through orchestrator
    result = await Runner.run(
        starting_agent=discovery_orchestrator,
        input=input_text,
        context=context,
        run_config=RunConfig(
            max_turns=20,
            workflow_name="Reddit Discovery",
            trace_metadata={"query": query or queries}
        )
    )
    
    return result.final_output
```

## Implementation Strategy

### Phase 1: Foundation (Week 1)
1. Set up project structure and dependencies
2. Create base models and context objects
3. Implement Search Executor and Validator agents
4. Basic integration tests

### Phase 2: Core Agents (Week 2)
1. Implement Query Analyzer with NLP tools
2. Create Subreddit Scorer with confidence metrics
3. Build Result Synthesizer
4. Add comprehensive testing

### Phase 3: Orchestration (Week 3)
1. Implement Discovery Orchestrator with routing logic
2. Create Batch Manager for parallel execution
3. Add handoff patterns and error handling
4. Integration with existing MCP server

### Phase 4: Optimization (Week 4)
1. Add caching layer
2. Optimize model selection per agent
3. Implement tracing and monitoring
4. Performance testing and tuning

## Benefits Over Current Implementation

1. **Modularity**: Each agent is independent and focused
2. **Scalability**: Easy to add new discovery strategies
3. **Observability**: Full tracing of decision process
4. **Testability**: Each agent can be unit tested
5. **Flexibility**: Agents can be reused in different workflows
6. **Performance**: Parallel execution and smart caching
7. **Maintainability**: Clear separation of concerns

## Migration Path

1. **Parallel Development**: Build new system alongside existing
2. **Feature Flag**: Toggle between old and new implementation
3. **Gradual Rollout**: Test with subset of queries first
4. **Backward Compatible**: Same interface as current discover.py
5. **Monitoring**: Compare results between old and new

## Testing Strategy

### Unit Tests
- Each agent tested independently
- Mock Reddit client and context
- Test all tools and handoffs

### Integration Tests
- End-to-end discovery workflows
- Multiple query types
- Error scenarios

### Performance Tests
- API call optimization
- Caching effectiveness
- Parallel execution benefits

## Monitoring and Observability

1. **Tracing**: Full agent decision tree
2. **Metrics**: API calls, latency, cache hits
3. **Logging**: Structured logs per agent
4. **Debugging**: Replay agent conversations

## Future Enhancements

1. **Learning**: Agents improve from feedback
2. **Personalization**: User-specific discovery preferences
3. **Advanced NLP**: Better query understanding
4. **Community Graph**: Relationship mapping between subreddits
5. **Trend Detection**: Identify emerging communities

## Conclusion

This agentic architecture transforms the monolithic discover.py into a flexible, scalable system of specialized agents. Each agent excels at its specific task while the orchestrator ensures optimal routing and efficiency. The result is a more maintainable, testable, and powerful discovery system that can evolve with changing requirements.