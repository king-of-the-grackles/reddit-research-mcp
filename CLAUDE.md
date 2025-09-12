# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Reddit Research MCP Server - A Model Context Protocol (MCP) server that turns Reddit into a queryable research database. Built with FastMCP and the three-layer architecture pattern for AI agents.

## Development Commands

### Running the Server
```bash
# Run locally with Python
python src/server.py

# Build distribution
python -m build

# Package installation (development)
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_tools.py

# Run tests matching a pattern
pytest -k "search"

# Generate HTML coverage report
pytest --cov=src --cov-report=html
# Then open htmlcov/index.html in browser
```

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux

# Install dependencies with dev extras for testing
pip install -e ".[dev]"
```

## Architecture

### Three-Layer Pattern
The server implements a layered abstraction pattern for AI agent interactions:

1. **Discovery Layer** (`discover_operations()`) - Returns available operations and workflows
2. **Schema Layer** (`get_operation_schema()`) - Provides parameter requirements and examples
3. **Execution Layer** (`execute_operation()`) - Performs the actual Reddit API calls

This pattern enables AI agents to self-discover capabilities and understand requirements before execution.

### Core Components

- **src/server.py** - FastMCP server with three-layer tools and research workflow prompt
- **src/config.py** - Reddit API configuration and client initialization
- **src/chroma_client.py** - Vector database proxy for semantic search across 20,000+ subreddits
- **src/resources.py** - MCP resources registration (server info, documentation)
- **src/models.py** - Pydantic data models for Reddit content
- **src/tools/** - Individual tool implementations:
  - `discover.py` - Semantic subreddit discovery via ChromaDB
  - `search.py` - Reddit search functionality
  - `posts.py` - Post fetching (single and batch)
  - `comments.py` - Comment tree retrieval

### Key Design Decisions

1. **Vector Search for Discovery**: Pre-indexed subreddit embeddings enable semantic search beyond Reddit's 250-result API limit
2. **Batch Operations**: `fetch_multiple` reduces API calls by 70% when researching across communities
3. **Evidence-Based Reports**: Every research output includes Reddit URLs and upvote counts for citation
4. **Progressive Research**: 5-30 minute deep research cycles vs quick searches
5. **Hosted ChromaDB Proxy**: Authenticated vector search via Render.com deployment

## Testing

### Test Configuration
- **Framework**: pytest with fixtures in `tests/conftest.py`
- **Configuration Files**: 
  - `pytest.ini` - Test discovery and asyncio settings
  - `.coveragerc` - Coverage reporting configuration
- **Current Coverage**: ~25% (Phase 1 target: 50%)

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_tools.py

# Run specific test class
pytest tests/test_tools.py::TestSearchReddit

# Run tests matching a pattern
pytest -k "search"

# Generate HTML coverage report
pytest --cov=src --cov-report=html
# Then open htmlcov/index.html in browser
```

### Test Structure
```
tests/
├── conftest.py           # Shared fixtures and mock data
├── test_tools.py         # Tests for Reddit API tools
├── test_config.py        # (Phase 1) Config and client tests
├── test_discover.py      # (Phase 2) Discovery system tests
└── test_server.py        # (Phase 3) MCP server tests
```

### Available Fixtures
- `mock_reddit` - Basic mock Reddit client
- `mock_submission` - Mock Reddit post
- `mock_comment` - Mock Reddit comment
- `mock_subreddit` - Mock subreddit object
- `submission_factory` - Create custom mock submissions
- `comment_factory` - Create custom mock comments
- `mock_reddit_with_data` - Pre-configured Reddit client with test data
- `mock_chroma_client` - Mock ChromaDB client for vector search

### Test Coverage Roadmap
See `/specs/test-coverage-plan.md` and `/specs/phase1-test-implementation.md` for detailed plans.

## Configuration

### Required Environment Variables
- `REDDIT_CLIENT_ID` - Reddit app client ID
- `REDDIT_CLIENT_SECRET` - Reddit app secret
- `REDDIT_USER_AGENT` - User agent string (e.g., "MCP:reddit-research:v1.0")

### Optional Configuration
- `CHROMA_PROXY_URL` - ChromaDB proxy URL (defaults to hosted instance)
- `CHROMA_PROXY_API_KEY` - Authentication for vector search proxy

## MCP Integration

The server publishes to the MCP registry and can be connected via:
- Claude Code: `claude mcp add --scope local --transport http reddit-research-mcp https://reddit-research-mcp.fastmcp.app/mcp`
- Direct stdio: `python src/server.py`

## Research Workflow

The server includes a comprehensive research prompt template (`RESEARCH_WORKFLOW_PROMPT`) that guides AI agents through:
1. Discovery phase - Semantic search for relevant subreddits
2. Strategy selection - Based on confidence scores
3. Post gathering - Batch fetching from multiple communities
4. Deep dive - Comment analysis for high-engagement posts
5. Synthesis - Evidence-based report generation with citations

## Important Patterns

- All Reddit operations require the `reddit` client parameter except `discover_subreddits`
- Use confidence scores (0-1) from discovery to guide research depth
- Batch operations (`fetch_multiple`) for efficiency when analyzing multiple subreddits
- Always include Reddit URLs when citing content for verifiability
- Check for `[deleted]` or `[removed]` content in responses