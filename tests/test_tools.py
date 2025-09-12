import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, PropertyMock

# Add project root to Python path so relative imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.search import search_in_subreddit
from src.tools.posts import fetch_subreddit_posts, fetch_multiple_subreddits  
from src.tools.comments import fetch_submission_with_comments, parse_comment_tree


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


class TestSearchReddit:
    def test_search_reddit_success(self):
        """Test successful Reddit search."""
        mock_reddit = Mock()
        mock_submissions = [
            create_mock_submission(id="1", title="First Post"),
            create_mock_submission(id="2", title="Second Post")
        ]
        
        mock_reddit.subreddit.return_value.search.return_value = mock_submissions
        
        result = search_in_subreddit(
            subreddit_name="all",
            query="test query",
            reddit=mock_reddit,
            limit=10
        )
        
        assert "results" in result
        assert result["count"] == 2
        assert result["results"][0]["title"] == "First Post"
        assert result["results"][1]["title"] == "Second Post"
    
    def test_search_reddit_subreddit_not_found(self):
        """Test search with failed request."""
        from prawcore import NotFound
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = NotFound(Mock())
        
        result = search_in_subreddit(
            subreddit_name="all",
            query="test",
            reddit=mock_reddit
        )
        
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_search_reddit_forbidden_subreddit(self):
        """Test search in forbidden/private subreddit."""
        from prawcore import Forbidden
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = Forbidden(Mock())
        
        result = search_in_subreddit(
            subreddit_name="private_sub",
            query="test query",
            reddit=mock_reddit
        )
        
        assert "error" in result
        assert "forbidden" in result["error"].lower()
    
    def test_search_reddit_generic_exception(self):
        """Test handling of unexpected exceptions."""
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = Exception("Unexpected error occurred")
        
        result = search_in_subreddit(
            subreddit_name="test",
            query="test query",
            reddit=mock_reddit
        )
        
        assert "error" in result
        assert "unexpected error" in result["error"].lower()


class TestFetchSubredditPosts:
    def test_fetch_posts_success(self):
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
            limit=10
        )
        
        assert "posts" in result
        assert "subreddit" in result
        assert result["count"] == 2
        assert result["subreddit"]["name"] == "test"
        assert result["posts"][0]["title"] == "Hot Post 1"
    
    def test_fetch_posts_invalid_subreddit(self):
        """Test fetching from non-existent subreddit."""
        from prawcore import NotFound
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = NotFound(Mock())
        
        result = fetch_subreddit_posts(
            subreddit_name="nonexistent",
            reddit=mock_reddit
        )
        
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_fetch_multiple_subreddits_success(self):
        """Test fetching posts from multiple subreddits."""
        mock_reddit = Mock()
        
        # Create mock submissions from different subreddits
        mock_posts = [
            create_mock_submission(id="1", title="Python Post"),
            create_mock_submission(id="2", title="Learn Python Post"),
            create_mock_submission(id="3", title="Another Python Post")
        ]
        
        # Set different subreddit names for each post
        mock_posts[0].subreddit.display_name = "python"
        mock_posts[1].subreddit.display_name = "learnpython"
        mock_posts[2].subreddit.display_name = "python"
        
        # Mock the multi-subreddit object
        mock_multi_subreddit = Mock()
        mock_multi_subreddit.hot.return_value = mock_posts
        mock_reddit.subreddit.return_value = mock_multi_subreddit
        
        result = fetch_multiple_subreddits(
            subreddit_names=["python", "learnpython"],
            reddit=mock_reddit,
            listing_type="hot",
            limit_per_subreddit=2
        )
        
        assert "posts_by_subreddit" in result
        assert "subreddits_found" in result
        assert set(result["subreddits_found"]) == {"python", "learnpython"}
        assert result["total_posts"] == 3
        assert len(result["posts_by_subreddit"]["python"]) == 2
        assert len(result["posts_by_subreddit"]["learnpython"]) == 1
    
    @pytest.mark.parametrize("listing_type", ["hot", "new", "rising", "top"])
    def test_fetch_posts_listing_types(self, listing_type):
        """Test all listing types work correctly."""
        mock_reddit = Mock()
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.subscribers = 1000000
        mock_subreddit.public_description = "Test subreddit"
        
        mock_posts = [create_mock_submission(id="1", title=f"{listing_type} Post")]
        
        # Set up the appropriate method for each listing type
        setattr(mock_subreddit, listing_type, Mock(return_value=mock_posts))
        if listing_type == "top":
            # Special case for top - needs time_filter
            mock_subreddit.top.return_value = mock_posts
        
        mock_reddit.subreddit.return_value = mock_subreddit
        
        result = fetch_subreddit_posts(
            subreddit_name="test",
            reddit=mock_reddit,
            listing_type=listing_type,
            time_filter="all" if listing_type == "top" else None,
            limit=10
        )
        
        assert "posts" in result
        assert result["count"] == 1
        assert result["posts"][0]["title"] == f"{listing_type} Post"
        
        # Verify the correct method was called
        if listing_type == "top":
            mock_subreddit.top.assert_called_once_with(time_filter="all", limit=10)
        else:
            getattr(mock_subreddit, listing_type).assert_called_once_with(limit=10)
    
    def test_fetch_posts_forbidden_subreddit(self):
        """Test handling of private/forbidden subreddits."""
        from prawcore import Forbidden
        mock_reddit = Mock()
        mock_subreddit = Mock()
        
        # Make display_name raise Forbidden when accessed
        type(mock_subreddit).display_name = PropertyMock(side_effect=Forbidden(Mock()))
        mock_reddit.subreddit.return_value = mock_subreddit
        
        result = fetch_subreddit_posts(
            subreddit_name="private",
            reddit=mock_reddit
        )
        
        assert "error" in result
        assert "forbidden" in result["error"].lower()
        assert "private" in result["error"].lower()
    
    def test_fetch_posts_invalid_listing_type(self):
        """Test error for invalid listing type."""
        mock_reddit = Mock()
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.subscribers = 1000000
        mock_subreddit.public_description = "Test subreddit"
        
        mock_reddit.subreddit.return_value = mock_subreddit
        
        result = fetch_subreddit_posts(
            subreddit_name="test",
            reddit=mock_reddit,
            listing_type="invalid_type",  # Invalid listing type
            limit=10
        )
        
        assert "error" in result
        assert "invalid listing_type" in result["error"].lower()
    
    def test_fetch_posts_top_with_time_filter(self):
        """Test time_filter parameter for top posts."""
        mock_reddit = Mock()
        mock_subreddit = Mock()
        mock_subreddit.display_name = "test"
        mock_subreddit.subscribers = 1000000
        mock_subreddit.public_description = "Test subreddit"
        
        mock_posts = [create_mock_submission(id="1", title="Top Post")]
        mock_subreddit.top.return_value = mock_posts
        
        mock_reddit.subreddit.return_value = mock_subreddit
        
        result = fetch_subreddit_posts(
            subreddit_name="test",
            reddit=mock_reddit,
            listing_type="top",
            time_filter="week",
            limit=25
        )
        
        assert "posts" in result
        assert result["count"] == 1
        
        # Verify top was called with correct time_filter
        mock_subreddit.top.assert_called_once_with(time_filter="week", limit=25)
    
    def test_fetch_posts_generic_exception(self):
        """Test handling of generic exceptions."""
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = Exception("Something went wrong")
        
        result = fetch_subreddit_posts(
            subreddit_name="test",
            reddit=mock_reddit
        )
        
        assert "error" in result
        assert "Failed to fetch posts" in result["error"]
    
    def test_fetch_multiple_subreddits_different_listing_types(self):
        """Test fetch_multiple_subreddits with different listing types."""
        mock_reddit = Mock()
        mock_multi_subreddit = Mock()
        
        # Create mock posts
        mock_posts = [create_mock_submission(id="1", title="New Post")]
        mock_posts[0].subreddit.display_name = "test"
        
        # Test each listing type
        for listing_type in ["new", "rising", "top"]:
            setattr(mock_multi_subreddit, listing_type, Mock(return_value=mock_posts))
        
        mock_reddit.subreddit.return_value = mock_multi_subreddit
        
        # Test "new" listing
        result = fetch_multiple_subreddits(
            subreddit_names=["test"],
            reddit=mock_reddit,
            listing_type="new",
            limit_per_subreddit=5
        )
        assert result["total_posts"] == 1
        mock_multi_subreddit.new.assert_called_once()
        
        # Test "rising" listing
        result = fetch_multiple_subreddits(
            subreddit_names=["test"],
            reddit=mock_reddit,
            listing_type="rising",
            limit_per_subreddit=5
        )
        mock_multi_subreddit.rising.assert_called_once()
        
        # Test "top" listing with time_filter
        result = fetch_multiple_subreddits(
            subreddit_names=["test"],
            reddit=mock_reddit,
            listing_type="top",
            time_filter="month",
            limit_per_subreddit=5
        )
        mock_multi_subreddit.top.assert_called_once_with(time_filter="month", limit=5)
    
    def test_fetch_multiple_subreddits_invalid_listing_type(self):
        """Test fetch_multiple_subreddits with invalid listing type."""
        mock_reddit = Mock()
        
        result = fetch_multiple_subreddits(
            subreddit_names=["test"],
            reddit=mock_reddit,
            listing_type="invalid",  # Invalid type
            limit_per_subreddit=5
        )
        
        assert "error" in result
        assert "Invalid listing_type" in result["error"]
    
    def test_fetch_multiple_subreddits_exception(self):
        """Test fetch_multiple_subreddits exception handling."""
        mock_reddit = Mock()
        mock_reddit.subreddit.side_effect = Exception("Network error")
        
        result = fetch_multiple_subreddits(
            subreddit_names=["test", "python"],
            reddit=mock_reddit,
            listing_type="hot",
            limit_per_subreddit=5
        )
        
        assert "error" in result
        assert "Failed to fetch from multiple subreddits" in result["error"]


class TestFetchSubmissionWithComments:
    def test_fetch_submission_success(self):
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
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="test123",
            comment_limit=10
        )
        
        assert "submission" in result
        assert "comments" in result
        assert result["submission"]["id"] == "test123"
        assert len(result["comments"]) == 2
        assert result["comments"][0]["body"] == "First comment"
    
    def test_fetch_submission_not_found(self):
        """Test fetching non-existent submission."""
        from prawcore import NotFound
        mock_reddit = Mock()
        mock_reddit.submission.side_effect = NotFound(Mock())
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="nonexistent"
        )
        
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_fetch_submission_no_id_or_url(self):
        """Test error when neither submission_id nor url is provided."""
        mock_reddit = Mock()
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit
        )
        
        assert "error" in result
        assert "submission_id or url must be provided" in result["error"]
    
    def test_parse_comment_tree(self):
        """Test recursive comment tree parsing."""
        from praw.models import Comment as PrawComment
        
        # Create nested comment structure
        root_comment = Mock(spec=PrawComment)
        root_comment.id = "root"
        root_comment.body = "Root comment"
        root_comment.author = Mock()
        root_comment.author.__str__ = Mock(return_value="rootuser")
        root_comment.score = 100
        root_comment.created_utc = 1234567890.0
        
        # Create reply
        reply1 = Mock(spec=PrawComment)
        reply1.id = "reply1"
        reply1.body = "First reply"
        reply1.author = Mock()
        reply1.author.__str__ = Mock(return_value="replyuser1")
        reply1.score = 50
        reply1.created_utc = 1234567891.0
        reply1.replies = []
        
        # Create nested reply
        reply1_1 = Mock(spec=PrawComment)
        reply1_1.id = "reply1_1"
        reply1_1.body = "Nested reply"
        reply1_1.author = Mock()
        reply1_1.author.__str__ = Mock(return_value="nesteduser")
        reply1_1.score = 25
        reply1_1.created_utc = 1234567892.0
        reply1_1.replies = []
        
        # Set up the reply structure
        reply1.replies = [reply1_1]
        root_comment.replies = [reply1]
        
        # Parse the comment tree
        parsed = parse_comment_tree(root_comment, depth=0, max_depth=3)
        
        assert parsed.id == "root"
        assert parsed.body == "Root comment"
        assert parsed.author == "rootuser"
        assert parsed.depth == 0
        assert len(parsed.replies) == 1
        
        # Check first reply
        assert parsed.replies[0].id == "reply1"
        assert parsed.replies[0].depth == 1
        assert len(parsed.replies[0].replies) == 1
        
        # Check nested reply
        assert parsed.replies[0].replies[0].id == "reply1_1"
        assert parsed.replies[0].replies[0].depth == 2
        assert len(parsed.replies[0].replies[0].replies) == 0
    
    def test_fetch_comments_deleted_author(self):
        """Test handling of deleted comment authors."""
        mock_reddit = Mock()
        mock_submission = create_mock_submission()
        
        # Create comment with deleted author
        mock_comment = create_mock_comment(id="c1", body="Comment from deleted user")
        mock_comment.author = None  # Deleted author
        
        mock_comments = Mock()
        mock_comments.__iter__ = Mock(return_value=iter([mock_comment]))
        mock_comments.replace_more = Mock()
        
        mock_submission.comments = mock_comments
        mock_submission.comment_sort = "best"
        
        mock_reddit.submission.return_value = mock_submission
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="test123"
        )
        
        assert "comments" in result
        assert result["comments"][0]["author"] == "[deleted]"
    
    def test_fetch_submission_by_url(self):
        """Test fetching submission by URL instead of ID."""
        mock_reddit = Mock()
        mock_submission = create_mock_submission()
        
        mock_comments = Mock()
        mock_comments.__iter__ = Mock(return_value=iter([]))
        mock_comments.replace_more = Mock()
        mock_submission.comments = mock_comments
        mock_submission.comment_sort = "best"
        
        mock_reddit.submission.return_value = mock_submission
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            url="https://reddit.com/r/test/comments/test123/"
        )
        
        assert "submission" in result
        assert result["submission"]["id"] == "test123"
        
        # Verify submission was called with url parameter
        mock_reddit.submission.assert_called_once_with(url="https://reddit.com/r/test/comments/test123/")
    
    def test_fetch_comments_forbidden_submission(self):
        """Test handling of forbidden/private submissions."""
        from prawcore import Forbidden
        mock_reddit = Mock()
        mock_reddit.submission.side_effect = Forbidden(Mock())
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="private123"
        )
        
        assert "error" in result
        assert "forbidden" in result["error"].lower()
    
    def test_fetch_comments_with_limit(self):
        """Test comment_limit parameter works."""
        mock_reddit = Mock()
        mock_submission = create_mock_submission()
        
        # Create multiple comments
        mock_comments_list = [
            create_mock_comment(id=f"c{i}", body=f"Comment {i}")
            for i in range(5)
        ]
        
        mock_comments = Mock()
        mock_comments.__iter__ = Mock(return_value=iter(mock_comments_list))
        mock_comments.replace_more = Mock()
        
        mock_submission.comments = mock_comments
        mock_submission.comment_sort = "best"
        
        mock_reddit.submission.return_value = mock_submission
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="test123",
            comment_limit=3  # Limit to 3 comments
        )
        
        assert "comments" in result
        assert len(result["comments"]) == 3  # Should stop at limit
    
    def test_fetch_comments_generic_exception(self):
        """Test handling of generic exceptions in fetch_submission_with_comments."""
        mock_reddit = Mock()
        mock_reddit.submission.side_effect = Exception("Network timeout")
        
        result = fetch_submission_with_comments(
            reddit=mock_reddit,
            submission_id="test123"
        )
        
        assert "error" in result
        assert "Invalid submission reference" in result["error"]
    
    def test_parse_comment_tree_with_praw_comment(self):
        """Test parse_comment_tree with actual PrawComment type."""
        from praw.models import Comment as PrawComment
        
        # Create a mock comment that is an instance of PrawComment
        mock_comment = Mock(spec=PrawComment)
        mock_comment.id = "praw123"
        mock_comment.body = "PRAW comment"
        mock_comment.author = Mock()
        mock_comment.author.__str__ = Mock(return_value="prawuser")
        mock_comment.score = 75
        mock_comment.created_utc = 1234567890.0
        mock_comment.replies = []
        
        # Parse the comment
        parsed = parse_comment_tree(mock_comment)
        
        assert parsed.id == "praw123"
        assert parsed.body == "PRAW comment"
        assert parsed.author == "prawuser"
        assert parsed.score == 75
    
    def test_count_replies_helper(self):
        """Test the count_replies helper function."""
        from src.tools.comments import count_replies
        from src.models import Comment
        
        # Create a comment tree
        root = Comment(
            id="root",
            body="Root",
            author="user1",
            score=100,
            created_utc=1234567890.0,
            depth=0,
            replies=[
                Comment(
                    id="r1",
                    body="Reply 1",
                    author="user2",
                    score=50,
                    created_utc=1234567891.0,
                    depth=1,
                    replies=[
                        Comment(
                            id="r1_1",
                            body="Nested",
                            author="user3",
                            score=25,
                            created_utc=1234567892.0,
                            depth=2,
                            replies=[]
                        )
                    ]
                ),
                Comment(
                    id="r2",
                    body="Reply 2",
                    author="user4",
                    score=30,
                    created_utc=1234567893.0,
                    depth=1,
                    replies=[]
                )
            ]
        )
        
        # Count replies
        count = count_replies(root)
        assert count == 3  # r1, r1_1, and r2