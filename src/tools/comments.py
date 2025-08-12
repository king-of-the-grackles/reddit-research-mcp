from typing import Optional, Dict, Any, Literal, List
import praw
from praw.models import Submission, Comment as PrawComment, MoreComments
from prawcore import NotFound, Forbidden
from ..models import SubmissionWithCommentsResult, RedditPost, Comment


def parse_comment_tree(
    comment: PrawComment,
    depth: int = 0,
    max_depth: int = 10
) -> Comment:
    """
    Recursively parse a comment and its replies into our Comment model.
    
    Args:
        comment: PRAW comment object
        depth: Current depth in the comment tree
        max_depth: Maximum depth to traverse
    
    Returns:
        Parsed Comment object with nested replies
    """
    replies = []
    if depth < max_depth and hasattr(comment, 'replies'):
        for reply in comment.replies:
            if isinstance(reply, PrawComment):
                replies.append(parse_comment_tree(reply, depth + 1, max_depth))
            # Skip MoreComments objects for simplicity in MVP
    
    return Comment(
        id=comment.id,
        body=comment.body,
        author=str(comment.author) if comment.author else "[deleted]",
        score=comment.score,
        created_utc=comment.created_utc,
        depth=depth,
        replies=replies
    )


def fetch_submission_with_comments(
    reddit: praw.Reddit,
    submission_id: Optional[str] = None,
    url: Optional[str] = None,
    comment_limit: int = 100,
    comment_sort: Literal["best", "top", "new"] = "best"
) -> Dict[str, Any]:
    """
    Fetch a Reddit submission with its comment tree.
    
    Args:
        reddit: Configured Reddit client
        submission_id: Reddit post ID
        url: Full URL to the post (alternative to submission_id)
        comment_limit: Maximum number of comments to fetch
        comment_sort: How to sort comments
    
    Returns:
        Dictionary containing submission and comments
    """
    try:
        # Validate that we have either submission_id or url
        if not submission_id and not url:
            return {"error": "Either submission_id or url must be provided"}
        
        # Get submission
        try:
            if submission_id:
                submission = reddit.submission(id=submission_id)
            else:
                submission = reddit.submission(url=url)
            
            # Force fetch to check if submission exists
            _ = submission.title
        except NotFound:
            return {"error": "Submission not found"}
        except Forbidden:
            return {"error": "Access to submission forbidden"}
        except Exception as e:
            return {"error": f"Invalid submission reference: {str(e)}"}
        
        # Set comment sort
        submission.comment_sort = comment_sort
        
        # Replace "More Comments" with actual comments (up to limit)
        submission.comments.replace_more(limit=0)  # Don't expand "more" comments in MVP
        
        # Parse submission
        submission_data = RedditPost(
            id=submission.id,
            title=submission.title,
            selftext=submission.selftext if submission.selftext else "",
            author=str(submission.author) if submission.author else "[deleted]",
            subreddit=submission.subreddit.display_name,
            score=submission.score,
            upvote_ratio=submission.upvote_ratio,
            num_comments=submission.num_comments,
            created_utc=submission.created_utc,
            url=submission.url
        )
        
        # Parse comments
        comments = []
        comment_count = 0
        
        for top_level_comment in submission.comments:
            # In tests, we might get regular Mock objects instead of PrawComment
            # Check if it has the required attributes
            if hasattr(top_level_comment, 'id') and hasattr(top_level_comment, 'body'):
                if comment_count >= comment_limit:
                    break
                if isinstance(top_level_comment, PrawComment):
                    comments.append(parse_comment_tree(top_level_comment))
                else:
                    # Handle mock objects in tests
                    comments.append(Comment(
                        id=top_level_comment.id,
                        body=top_level_comment.body,
                        author=str(top_level_comment.author) if top_level_comment.author else "[deleted]",
                        score=top_level_comment.score,
                        created_utc=top_level_comment.created_utc,
                        depth=0,
                        replies=[]
                    ))
                # Count all comments including replies
                comment_count += 1 + count_replies(comments[-1])
        
        result = SubmissionWithCommentsResult(
            submission=submission_data,
            comments=comments,
            total_comments_fetched=comment_count
        )
        
        return result.model_dump()
        
    except Exception as e:
        return {"error": f"Failed to fetch submission: {str(e)}"}


def count_replies(comment: Comment) -> int:
    """Count total number of replies in a comment tree."""
    count = len(comment.replies)
    for reply in comment.replies:
        count += count_replies(reply)
    return count