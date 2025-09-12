import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def mock_reddit():
    """Fixture for a mock Reddit client."""
    reddit = Mock()
    reddit.user = Mock()
    reddit.user.me = Mock(return_value=Mock(name="test_user"))
    return reddit


@pytest.fixture
def mock_submission():
    """Fixture for a mock Reddit submission with default values."""
    submission = Mock()
    submission.id = "test123"
    submission.title = "Test Post Title"
    submission.author = Mock()
    submission.author.__str__ = Mock(return_value="testuser")
    submission.score = 100
    submission.num_comments = 50
    submission.created_utc = 1234567890.0
    submission.url = "https://reddit.com/r/test/test123"
    submission.selftext = "Test post content"
    submission.upvote_ratio = 0.95
    submission.permalink = "/r/test/comments/test123/test_post_title/"
    submission.subreddit = Mock()
    submission.subreddit.display_name = "test"
    submission.link_flair_text = "Discussion"
    submission.over_18 = False
    submission.spoiler = False
    submission.stickied = False
    submission.locked = False
    submission.distinguished = None
    return submission


@pytest.fixture
def mock_comment():
    """Fixture for a mock Reddit comment with default values."""
    comment = Mock()
    comment.id = "comment123"
    comment.body = "This is a test comment"
    comment.author = Mock()
    comment.author.__str__ = Mock(return_value="commentuser")
    comment.score = 10
    comment.created_utc = 1234567890.0
    comment.replies = []
    comment.is_submitter = False
    comment.distinguished = None
    comment.edited = False
    comment.collapsed = False
    comment.depth = 0
    comment.permalink = "/r/test/comments/test123/test_post/comment123"
    return comment


@pytest.fixture
def mock_subreddit():
    """Fixture for a mock subreddit."""
    subreddit = Mock()
    subreddit.display_name = "test"
    subreddit.display_name_prefixed = "r/test"
    subreddit.subscribers = 1000000
    subreddit.active_user_count = 5000
    subreddit.public_description = "A test subreddit for testing"
    subreddit.description = "Full description of the test subreddit"
    subreddit.created_utc = 1234567890.0
    subreddit.over18 = False
    subreddit.spoilers_enabled = True
    subreddit.wiki_enabled = True
    subreddit.submission_type = "any"
    return subreddit


@pytest.fixture
def mock_chroma_client():
    """Fixture for a mock ChromaDB client."""
    with patch('src.chroma_client.ChromaProxyClient') as MockChroma:
        client = Mock()
        client.search_subreddits = Mock(return_value={
            "results": [
                {
                    "name": "python",
                    "description": "News about the dynamic, interpreted, interactive, object-oriented, extensible programming language Python",
                    "subscribers": 1200000,
                    "confidence": 0.95
                },
                {
                    "name": "learnpython", 
                    "description": "Subreddit for posting questions and asking for general advice about your python code.",
                    "subscribers": 800000,
                    "confidence": 0.85
                }
            ],
            "query": "python programming",
            "total_results": 2
        })
        MockChroma.return_value = client
        yield client


@pytest.fixture
def mock_praw_not_found():
    """Fixture that provides the prawcore NotFound exception."""
    from prawcore import NotFound
    response = Mock()
    response.status_code = 404
    return NotFound(response)


@pytest.fixture
def mock_praw_forbidden():
    """Fixture that provides the prawcore Forbidden exception."""
    from prawcore import Forbidden
    response = Mock()
    response.status_code = 403
    return Forbidden(response)


@pytest.fixture
def submission_factory():
    """Factory fixture for creating mock submissions with custom attributes."""
    def _create_submission(**kwargs):
        submission = Mock()
        defaults = {
            "id": "default123",
            "title": "Default Test Post",
            "author": Mock(),
            "score": 100,
            "num_comments": 50,
            "created_utc": 1234567890.0,
            "url": "https://reddit.com/r/test/default123",
            "selftext": "Default test content",
            "upvote_ratio": 0.95,
            "permalink": "/r/test/comments/default123/default_test_post/",
            "subreddit": Mock(),
            "link_flair_text": None,
            "over_18": False,
            "spoiler": False,
            "stickied": False,
            "locked": False,
            "distinguished": None
        }
        
        # Update defaults with provided kwargs
        for key, value in defaults.items():
            setattr(submission, key, kwargs.get(key, value))
        
        # Handle special cases
        if "author" in kwargs and isinstance(kwargs["author"], str):
            submission.author = Mock()
            submission.author.__str__ = Mock(return_value=kwargs["author"])
        elif not hasattr(submission.author, '__str__'):
            submission.author.__str__ = Mock(return_value="defaultuser")
            
        if "subreddit" in kwargs and isinstance(kwargs["subreddit"], str):
            submission.subreddit = Mock()
            submission.subreddit.display_name = kwargs["subreddit"]
        elif not hasattr(submission.subreddit, 'display_name'):
            submission.subreddit.display_name = "test"
            
        return submission
    
    return _create_submission


@pytest.fixture
def comment_factory():
    """Factory fixture for creating mock comments with custom attributes."""
    def _create_comment(**kwargs):
        comment = Mock()
        defaults = {
            "id": "defaultcomment",
            "body": "Default comment text",
            "author": Mock(),
            "score": 10,
            "created_utc": 1234567890.0,
            "replies": [],
            "is_submitter": False,
            "distinguished": None,
            "edited": False,
            "collapsed": False,
            "depth": 0,
            "permalink": "/r/test/comments/test123/test_post/defaultcomment"
        }
        
        # Update defaults with provided kwargs
        for key, value in defaults.items():
            setattr(comment, key, kwargs.get(key, value))
        
        # Handle special cases
        if "author" in kwargs and isinstance(kwargs["author"], str):
            comment.author = Mock()
            comment.author.__str__ = Mock(return_value=kwargs["author"])
        elif not hasattr(comment.author, '__str__'):
            comment.author.__str__ = Mock(return_value="defaultcommentuser")
            
        return comment
    
    return _create_comment


@pytest.fixture
def mock_reddit_with_data(mock_subreddit, submission_factory, comment_factory):
    """Fixture for a mock Reddit client with pre-configured test data."""
    reddit = Mock()
    
    # Create some test submissions
    submissions = [
        submission_factory(id="post1", title="First Test Post", score=500),
        submission_factory(id="post2", title="Second Test Post", score=300),
        submission_factory(id="post3", title="Third Test Post", score=100),
    ]
    
    # Create some test comments
    comments = [
        comment_factory(id="c1", body="Great post!", score=50),
        comment_factory(id="c2", body="I disagree", score=20),
        comment_factory(id="c3", body="Thanks for sharing", score=15),
    ]
    
    # Configure the mock Reddit client
    reddit.subreddit.return_value = mock_subreddit
    mock_subreddit.hot.return_value = submissions
    mock_subreddit.new.return_value = submissions
    mock_subreddit.top.return_value = submissions
    mock_subreddit.search.return_value = submissions[:2]
    
    # Configure submission with comments
    for submission in submissions:
        mock_comments = Mock()
        mock_comments.__iter__ = Mock(return_value=iter(comments))
        mock_comments.replace_more = Mock()
        submission.comments = mock_comments
    
    reddit.submission.return_value = submissions[0]
    reddit.user.me.return_value = Mock(name="test_user")
    
    return reddit