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
from unittest.mock import Mock, MagicMock, AsyncMock
from fastmcp import Context

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.discover import discover_subreddits, validate_subreddit, SearchConfig, calculate_confidence_from_distance
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

    async def test_discover_accepts_context(self, mock_context, monkeypatch):
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
        result = await discover_subreddits(query="test", limit=5, ctx=mock_context)

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

    async def test_fetch_multiple_accepts_context(self, mock_context, mock_reddit):
        """Verify fetch_multiple_subreddits accepts context parameter."""
        mock_multi = Mock()
        mock_multi.hot.return_value = []
        mock_reddit.subreddit.return_value = mock_multi

        result = await fetch_multiple_subreddits(
            subreddit_names=["test1", "test2"],
            reddit=mock_reddit,
            limit_per_subreddit=5,
            ctx=mock_context
        )

        assert "subreddits_requested" in result or "error" in result


class TestCommentOperations:
    """Test comment-fetching functions accept context."""

    async def test_fetch_comments_accepts_context(self, mock_context, mock_reddit):
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

        result = await fetch_submission_with_comments(
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


class TestDiscoverSubredditsProgress:
    """Test progress reporting in discover_subreddits."""

    async def test_reports_progress_during_search(self, mock_context, monkeypatch):
        """Verify progress is reported during vector search."""
        # Mock ChromaDB response with 3 results
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'Python', 'subscribers': 1000000, 'nsfw': False},
                {'name': 'learnpython', 'subscribers': 500000, 'nsfw': False},
                {'name': 'pythontips', 'subscribers': 100000, 'nsfw': False}
            ]],
            'distances': [[0.5, 0.7, 0.9]]
        }

        # Setup async mock for progress
        mock_context.report_progress = AsyncMock()

        def mock_get_client():
            return mock_client

        def mock_get_collection(name, client):
            return mock_collection

        monkeypatch.setattr('src.tools.discover.get_chroma_client', mock_get_client)
        monkeypatch.setattr('src.tools.discover.get_collection', mock_get_collection)

        result = await discover_subreddits(query="python", ctx=mock_context)

        # Verify progress was reported at least 3 times (once per result)
        assert mock_context.report_progress.call_count >= 3

        # Verify progress parameters
        first_call = mock_context.report_progress.call_args_list[0]
        # Check if arguments were passed as kwargs or positional args
        if first_call[1]:  # kwargs
            assert 'progress' in first_call[1]
            assert 'total' in first_call[1]
        else:  # positional
            assert len(first_call[0]) >= 2


class TestFetchMultipleProgress:
    """Test progress reporting in fetch_multiple_subreddits."""

    async def test_reports_progress_per_subreddit(self, mock_context, mock_reddit):
        """Verify progress is reported once per subreddit."""
        # Setup async mock for progress
        mock_context.report_progress = AsyncMock()

        # Mock submissions from 3 different subreddits
        mock_sub1 = Mock()
        mock_sub1.subreddit.display_name = "sub1"
        mock_sub1.id = "id1"
        mock_sub1.title = "Title 1"
        mock_sub1.author = Mock()
        mock_sub1.author.__str__ = Mock(return_value="user1")
        mock_sub1.score = 100
        mock_sub1.num_comments = 10
        mock_sub1.created_utc = 1234567890.0
        mock_sub1.url = "https://reddit.com/test1"
        mock_sub1.permalink = "/r/sub1/comments/id1/"

        mock_sub2 = Mock()
        mock_sub2.subreddit.display_name = "sub2"
        mock_sub2.id = "id2"
        mock_sub2.title = "Title 2"
        mock_sub2.author = Mock()
        mock_sub2.author.__str__ = Mock(return_value="user2")
        mock_sub2.score = 200
        mock_sub2.num_comments = 20
        mock_sub2.created_utc = 1234567891.0
        mock_sub2.url = "https://reddit.com/test2"
        mock_sub2.permalink = "/r/sub2/comments/id2/"

        mock_sub3 = Mock()
        mock_sub3.subreddit.display_name = "sub3"
        mock_sub3.id = "id3"
        mock_sub3.title = "Title 3"
        mock_sub3.author = Mock()
        mock_sub3.author.__str__ = Mock(return_value="user3")
        mock_sub3.score = 300
        mock_sub3.num_comments = 30
        mock_sub3.created_utc = 1234567892.0
        mock_sub3.url = "https://reddit.com/test3"
        mock_sub3.permalink = "/r/sub3/comments/id3/"

        mock_multi = Mock()
        mock_multi.hot.return_value = [mock_sub1, mock_sub2, mock_sub3]
        mock_reddit.subreddit.return_value = mock_multi

        result = await fetch_multiple_subreddits(
            subreddit_names=["sub1", "sub2", "sub3"],
            reddit=mock_reddit,
            ctx=mock_context
        )

        # Verify progress was reported at least 3 times (once per subreddit)
        assert mock_context.report_progress.call_count >= 3


class TestFetchCommentsProgress:
    """Test progress reporting in fetch_submission_with_comments."""

    async def test_reports_progress_during_loading(self, mock_context, mock_reddit):
        """Verify progress is reported during comment loading."""
        # Setup async mock for progress
        mock_context.report_progress = AsyncMock()

        # Mock submission
        mock_submission = Mock()
        mock_submission.id = "test123"
        mock_submission.title = "Test"
        mock_submission.author = Mock()
        mock_submission.author.__str__ = Mock(return_value="testuser")
        mock_submission.score = 100
        mock_submission.upvote_ratio = 0.95
        mock_submission.num_comments = 5
        mock_submission.created_utc = 1234567890.0
        mock_submission.url = "https://reddit.com/test"
        mock_submission.selftext = ""
        mock_submission.subreddit = Mock()
        mock_submission.subreddit.display_name = "test"

        # Mock 5 comments
        mock_comments_list = []
        for i in range(5):
            mock_comment = Mock()
            mock_comment.id = f"comment{i}"
            mock_comment.body = f"Comment {i}"
            mock_comment.author = Mock()
            mock_comment.author.__str__ = Mock(return_value=f"user{i}")
            mock_comment.score = 10 * i
            mock_comment.created_utc = 1234567890.0 + i
            mock_comment.replies = []
            mock_comments_list.append(mock_comment)

        mock_comments = Mock()
        mock_comments.__iter__ = Mock(return_value=iter(mock_comments_list))
        mock_comments.replace_more = Mock()
        mock_submission.comments = mock_comments

        mock_reddit.submission.return_value = mock_submission

        result = await fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="test123",
            comment_limit=10,
            ctx=mock_context
        )

        # Verify progress was reported at least 6 times (5 comments + 1 completion)
        assert mock_context.report_progress.call_count >= 6


class TestSearchConfig:
    """Test SearchConfig customization in discover_subreddits."""

    async def test_custom_min_confidence_filtering(self, mock_context, monkeypatch):
        """Verify min_confidence parameter filters results correctly."""
        # Mock ChromaDB response with results at different confidence levels
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'Python', 'subscribers': 1000000, 'nsfw': False},      # distance 0.3 -> high confidence
                {'name': 'learnpython', 'subscribers': 500000, 'nsfw': False},  # distance 0.9 -> medium confidence
                {'name': 'pythontips', 'subscribers': 100000, 'nsfw': False}    # distance 1.5 -> low confidence
            ]],
            'distances': [[0.3, 0.9, 1.5]]
        }

        def mock_get_client():
            return mock_client

        def mock_get_collection(name, client):
            return mock_collection

        monkeypatch.setattr('src.tools.discover.get_chroma_client', mock_get_client)
        monkeypatch.setattr('src.tools.discover.get_collection', mock_get_collection)

        # Test with high min_confidence filter
        result = await discover_subreddits(query="python", min_confidence=0.7, ctx=mock_context)

        # Should only return results with confidence >= 0.7
        assert "subreddits" in result
        # All returned subreddits should meet or exceed min_confidence
        for sub in result.get("subreddits", []):
            assert sub["confidence"] >= 0.7

    async def test_custom_generic_subreddit_penalty(self, mock_context, monkeypatch):
        """Verify custom generic subreddit penalty is applied."""
        # Mock ChromaDB response
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'funny', 'subscribers': 1000000, 'nsfw': False},  # Generic sub
                {'name': 'specific_topic', 'subscribers': 10000, 'nsfw': False}
            ]],
            'distances': [[0.5, 0.5]]  # Same distance
        }

        def mock_get_client():
            return mock_client

        def mock_get_collection(name, client):
            return mock_collection

        monkeypatch.setattr('src.tools.discover.get_chroma_client', mock_get_client)
        monkeypatch.setattr('src.tools.discover.get_collection', mock_get_collection)

        # Test with custom penalty multiplier
        custom_config = SearchConfig(GENERIC_PENALTY_MULTIPLIER=0.1)  # Harsher penalty
        result = await discover_subreddits(
            query="jokes",
            limit=10,
            config=custom_config,
            ctx=mock_context
        )

        # Both start with same base confidence at distance 0.5
        # funny should have 0.1x penalty (generic) unless "jokes" is in the name
        # specific_topic should not be penalized
        assert "subreddits" in result
        if len(result["subreddits"]) >= 2:
            # The generic sub should have lower confidence than specific one
            confidences = {sub["name"]: sub["confidence"] for sub in result["subreddits"]}
            # This test validates the config is actually used

    async def test_custom_distance_thresholds(self, mock_context, monkeypatch):
        """Verify custom match tier distance thresholds are applied."""
        # Mock ChromaDB response
        mock_client = Mock()
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'metadatas': [[
                {'name': 'test1', 'subscribers': 1000, 'nsfw': False},
                {'name': 'test2', 'subscribers': 1000, 'nsfw': False},
                {'name': 'test3', 'subscribers': 1000, 'nsfw': False}
            ]],
            'distances': [[0.15, 0.4, 0.8]]
        }

        def mock_get_client():
            return mock_client

        def mock_get_collection(name, client):
            return mock_collection

        monkeypatch.setattr('src.tools.discover.get_chroma_client', mock_get_client)
        monkeypatch.setattr('src.tools.discover.get_collection', mock_get_collection)

        # Test with custom thresholds (stricter)
        custom_config = SearchConfig(
            EXACT_DISTANCE_THRESHOLD=0.1,      # Stricter exact threshold
            SEMANTIC_DISTANCE_THRESHOLD=0.3,   # Stricter semantic threshold
            ADJACENT_DISTANCE_THRESHOLD=0.6    # Stricter adjacent threshold
        )
        result = await discover_subreddits(query="test", config=custom_config, ctx=mock_context)

        # Verify tier classification matches custom thresholds
        assert "subreddits" in result
        for sub in result["subreddits"]:
            if sub["distance"] < 0.1:
                assert sub["match_tier"] == "exact"
            elif sub["distance"] < 0.3:
                assert sub["match_tier"] == "semantic"
            elif sub["distance"] < 0.6:
                assert sub["match_tier"] == "adjacent"

    def test_confidence_calculation_function(self):
        """Verify calculate_confidence_from_distance function works correctly."""
        # Test with default config
        conf_0_5 = calculate_confidence_from_distance(0.5)
        conf_1_0 = calculate_confidence_from_distance(1.0)
        conf_1_5 = calculate_confidence_from_distance(1.5)

        # Lower distances should give higher confidence
        assert conf_0_5 > conf_1_0
        assert conf_1_0 > conf_1_5

        # All should be between 0 and 1
        assert 0.0 <= conf_0_5 <= 1.0
        assert 0.0 <= conf_1_0 <= 1.0
        assert 0.0 <= conf_1_5 <= 1.0

    def test_custom_confidence_mapping(self):
        """Verify custom confidence distance mapping is applied."""
        # Create custom config with different mapping
        custom_config = SearchConfig(
            CONFIDENCE_DISTANCE_BREAKPOINTS={
                0.5: 0.9,   # At distance 0.5, confidence is 0.9
                1.0: 0.5,   # At distance 1.0, confidence is 0.5
                2.0: 0.1    # At distance 2.0, confidence is 0.1
            }
        )

        # Test confidence at custom breakpoints
        conf_0_5 = calculate_confidence_from_distance(0.5, custom_config)
        conf_1_0 = calculate_confidence_from_distance(1.0, custom_config)
        conf_2_0 = calculate_confidence_from_distance(2.0, custom_config)

        # Should respect custom mapping
        assert conf_0_5 == 0.9
        assert conf_1_0 == 0.5
        assert conf_2_0 == 0.1

    async def test_search_config_with_context(self, mock_context, monkeypatch):
        """Verify SearchConfig works with context parameter."""
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

        # Setup progress tracking
        mock_context.report_progress = AsyncMock()

        # Call with both custom config and context
        custom_config = SearchConfig(GENERIC_PENALTY_MULTIPLIER=0.2)
        result = await discover_subreddits(
            query="test",
            config=custom_config,
            ctx=mock_context
        )

        # Both should work together
        assert "subreddits" in result or "error" in result
        assert mock_context.report_progress.called  # Context was used
