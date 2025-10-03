"""
Integration tests for Context parameter acceptance in Phase 1.

This test suite verifies that all tool and operation functions
accept the Context parameter as required by FastMCP's Context API.
Phase 1 only validates parameter acceptance - actual context usage
will be tested in Phase 2+.
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock
from fastmcp import Context

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.discover import discover_subreddits, validate_subreddit
from src.tools.search import search_in_subreddit
from src.tools.posts import fetch_subreddit_posts, fetch_multiple_subreddits
from src.tools.comments import fetch_submission_with_comments


@pytest.fixture
def mock_context():
    """Create a mock Context object for testing."""
    return Mock(spec=Context)


@pytest.fixture
def mock_reddit():
    """Create a mock Reddit client."""
    return Mock()


@pytest.fixture
def mock_chroma():
    """Mock ChromaDB client and collection."""
    with Mock() as mock_client:
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'test', 'subscribers': 1000, 'url': 'https://reddit.com/r/test', 'nsfw': False}
            ]],
            'distances': [[0.5]]
        }
        yield mock_client, mock_collection


class TestDiscoverOperations:
    """Test discover_subreddits accepts context."""

    def test_discover_accepts_context(self, mock_context, monkeypatch):
        """Verify discover_subreddits accepts context parameter."""
        # Mock the chroma client
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'test', 'subscribers': 1000, 'url': 'https://reddit.com/r/test', 'nsfw': False}
            ]],
            'distances': [[0.5]]
        }

        def mock_get_client():
            return mock_client

        def mock_get_collection(name, client):
            return mock_collection

        monkeypatch.setattr('src.tools.discover.get_chroma_client', mock_get_client)
        monkeypatch.setattr('src.tools.discover.get_collection', mock_get_collection)

        # Call with context
        result = discover_subreddits(query="test", limit=5, ctx=mock_context)

        # Verify result structure (not context usage - that's Phase 2)
        assert "subreddits" in result or "error" in result


class TestSearchOperations:
    """Test search_in_subreddit accepts context."""

    def test_search_accepts_context(self, mock_context, mock_reddit):
        """Verify search_in_subreddit accepts context parameter."""
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.search.return_value = []
        mock_reddit.subreddit.return_value = mock_subreddit

        result = search_in_subreddit(
            subreddit_name="test",
            query="test query",
            reddit=mock_reddit,
            limit=5,
            ctx=mock_context
        )

        assert "results" in result or "error" in result


class TestPostOperations:
    """Test post-fetching functions accept context."""

    def test_fetch_posts_accepts_context(self, mock_context, mock_reddit):
        """Verify fetch_subreddit_posts accepts context parameter."""
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.subscribers = 1000
        mock_subreddit.public_description = "Test"
        mock_subreddit.hot.return_value = []
        mock_reddit.subreddit.return_value = mock_subreddit

        result = fetch_subreddit_posts(
            subreddit_name="test",
            reddit=mock_reddit,
            limit=5,
            ctx=mock_context
        )

        assert "posts" in result or "error" in result

    def test_fetch_multiple_accepts_context(self, mock_context, mock_reddit):
        """Verify fetch_multiple_subreddits accepts context parameter."""
        mock_multi = Mock()
        mock_multi.hot.return_value = []
        mock_reddit.subreddit.return_value = mock_multi

        result = fetch_multiple_subreddits(
            subreddit_names=["test1", "test2"],
            reddit=mock_reddit,
            limit_per_subreddit=5,
            ctx=mock_context
        )

        assert "subreddits_requested" in result or "error" in result


class TestCommentOperations:
    """Test comment-fetching functions accept context."""

    def test_fetch_comments_accepts_context(self, mock_context, mock_reddit):
        """Verify fetch_submission_with_comments accepts context parameter."""
        mock_submission = Mock()
        mock_submission.id = "test123"
        mock_submission.title = "Test"
        mock_submission.author = Mock()
        mock_submission.author.__str__ = Mock(return_value="testuser")
        mock_submission.score = 100
        mock_submission.upvote_ratio = 0.95
        mock_submission.num_comments = 0
        mock_submission.created_utc = 1234567890.0
        mock_submission.url = "https://reddit.com/test"
        mock_submission.selftext = ""
        mock_submission.subreddit = Mock()
        mock_submission.subreddit.display_name = "test"

        # Mock comments
        mock_comments = Mock()
        mock_comments.__iter__ = Mock(return_value=iter([]))
        mock_comments.replace_more = Mock()
        mock_submission.comments = mock_comments

        mock_reddit.submission.return_value = mock_submission

        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="test123",
            comment_limit=10,
            ctx=mock_context
        )

        assert "submission" in result or "error" in result


class TestHelperFunctions:
    """Test helper functions accept context."""

    def test_validate_subreddit_accepts_context(self, mock_context, monkeypatch):
        """Verify validate_subreddit accepts context parameter."""
        # Mock the chroma client
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'test', 'subscribers': 1000, 'nsfw': False}
            ]],
            'distances': [[0.5]]
        }

        def mock_get_client():
            return mock_client

        def mock_get_collection(name, client):
            return mock_collection

        monkeypatch.setattr('src.tools.discover.get_chroma_client', mock_get_client)
        monkeypatch.setattr('src.tools.discover.get_collection', mock_get_collection)

        result = validate_subreddit("test", ctx=mock_context)

        assert "valid" in result or "error" in result


class TestContextParameterPosition:
    """Test that context parameter works in various positions."""

    def test_context_as_last_param(self, mock_context, mock_reddit):
        """Verify context works as the last parameter."""
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.search.return_value = []
        mock_reddit.subreddit.return_value = mock_subreddit

        # Context is last parameter
        result = search_in_subreddit(
            subreddit_name="test",
            query="test",
            reddit=mock_reddit,
            sort="relevance",
            time_filter="all",
            limit=10,
            ctx=mock_context
        )

        assert result is not None

    def test_context_with_defaults(self, mock_context, mock_reddit):
        """Verify context works with default parameters."""
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.search.return_value = []
        mock_reddit.subreddit.return_value = mock_subreddit

        # Only required params + context
        result = search_in_subreddit(
            subreddit_name="test",
            query="test",
            reddit=mock_reddit,
            ctx=mock_context
        )

        assert result is not None
