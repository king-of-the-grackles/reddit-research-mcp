import pytest
import sys
import os
from unittest.mock import Mock, MagicMock
from fastmcp import Context

# Add project root to Python path so relative imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.search import search_in_subreddit
from src.tools.posts import fetch_subreddit_posts
from src.tools.comments import fetch_submission_with_comments


def create_mock_submission(
    id="test123",
    title="Test Post",
    author="testuser",
    score=100,
    num_comments=50
):
    """Helper to create a mock Reddit submission."""
    submission = Mock()
    submission.id = id
    submission.title = title
    submission.author = Mock()
    submission.author.__str__ = Mock(return_value=author)
    submission.score = score
    submission.num_comments = num_comments
    submission.created_utc = 1234567890.0
    submission.url = f"https://reddit.com/r/test/{id}"
    submission.selftext = "Test content"
    submission.upvote_ratio = 0.95
    submission.permalink = f"/r/test/comments/{id}/test_post/"
    submission.subreddit = Mock()
    submission.subreddit.display_name = "test"
    return submission


def create_mock_comment(
    id="comment123",
    body="Test comment",
    author="commentuser",
    score=10
):
    """Helper to create a mock Reddit comment."""
    comment = Mock()
    comment.id = id
    comment.body = body
    comment.author = Mock()
    comment.author.__str__ = Mock(return_value=author)
    comment.score = score
    comment.created_utc = 1234567890.0
    comment.replies = []
    return comment


@pytest.fixture
def mock_context():
    """Create a mock Context object for testing."""
    return Mock(spec=Context)


class TestSearchReddit:
    def test_search_reddit_success(self, mock_context):
        """Test successful Reddit search."""
        mock_reddit = Mock()
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_submissions = [
            create_mock_submission(id="1", title="First Post"),
            create_mock_submission(id="2", title="Second Post")
        ]

        mock_subreddit.search.return_value = mock_submissions
        mock_reddit.subreddit.return_value = mock_subreddit

        result = search_in_subreddit(
            subreddit_name="test",
            query="test query",
            reddit=mock_reddit,
            limit=10,
            ctx=mock_context
        )

        assert "results" in result
        assert result["count"] == 2
        assert result["results"][0]["title"] == "First Post"
        assert result["results"][1]["title"] == "Second Post"

    def test_search_reddit_subreddit_not_found(self, mock_context):
        """Test search with failed request."""
        from prawcore import NotFound
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = NotFound(Mock())

        result = search_in_subreddit(
            subreddit_name="test",
            query="test",
            reddit=mock_reddit,
            ctx=mock_context
        )

        assert "error" in result
        assert "not found" in result["error"].lower()


class TestFetchSubredditPosts:
    def test_fetch_posts_success(self, mock_context):
        """Test successful fetching of subreddit posts."""
        mock_reddit = Mock()
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.subscribers = 1000000
        mock_subreddit.public_description = "Test subreddit"

        mock_posts = [
            create_mock_submission(id="1", title="Hot Post 1"),
            create_mock_submission(id="2", title="Hot Post 2")
        ]

        mock_subreddit.hot.return_value = mock_posts
        mock_reddit.subreddit.return_value = mock_subreddit

        result = fetch_subreddit_posts(
            subreddit_name="test",
            reddit=mock_reddit,
            listing_type="hot",
            limit=10,
            ctx=mock_context
        )

        assert "posts" in result
        assert "subreddit" in result
        assert result["count"] == 2
        assert result["subreddit"]["name"] == "test"
        assert result["posts"][0]["title"] == "Hot Post 1"

    def test_fetch_posts_invalid_subreddit(self, mock_context):
        """Test fetching from non-existent subreddit."""
        from prawcore import NotFound
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = NotFound(Mock())

        result = fetch_subreddit_posts(
            subreddit_name="nonexistent",
            reddit=mock_reddit,
            ctx=mock_context
        )

        assert "error" in result
        assert "not found" in result["error"].lower()


class TestFetchSubmissionWithComments:
    async def test_fetch_submission_success(self, mock_context):
        """Test successful fetching of submission with comments."""
        mock_reddit = Mock()
        mock_submission = create_mock_submission()

        # Create mock comments
        mock_comment1 = create_mock_comment(id="c1", body="First comment")
        mock_comment2 = create_mock_comment(id="c2", body="Second comment")

        # Create a mock comments object that behaves like a list but has replace_more
        mock_comments = Mock()
        mock_comments.__iter__ = Mock(return_value=iter([mock_comment1, mock_comment2]))
        mock_comments.replace_more = Mock()

        mock_submission.comments = mock_comments
        mock_submission.comment_sort = "best"

        mock_reddit.submission.return_value = mock_submission

        result = await fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="test123",
            comment_limit=10,
            ctx=mock_context
        )

        assert "submission" in result
        assert "comments" in result
        assert result["submission"]["id"] == "test123"
        assert len(result["comments"]) == 2
        assert result["comments"][0]["body"] == "First comment"

    async def test_fetch_submission_not_found(self, mock_context):
        """Test fetching non-existent submission."""
        from prawcore import NotFound
        mock_reddit = Mock()
        mock_reddit.submission.side_effect = NotFound(Mock())

        result = await fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="nonexistent",
            ctx=mock_context
        )

        assert "error" in result
        assert "not found" in result["error"].lower()

    async def test_fetch_submission_no_id_or_url(self, mock_context):
        """Test error when neither submission_id nor url is provided."""
        mock_reddit = Mock()

        result = await fetch_submission_with_comments(
            reddit=mock_reddit,
            ctx=mock_context
        )

        assert "error" in result
        assert "submission_id or url must be provided" in result["error"]