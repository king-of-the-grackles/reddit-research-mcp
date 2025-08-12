from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class RedditPost(BaseModel):
    """Model for a Reddit post/submission."""
    id: str
    title: str
    author: str
    subreddit: str
    score: int
    created_utc: float
    url: str
    num_comments: int
    selftext: Optional[str] = None
    upvote_ratio: Optional[float] = None
    permalink: Optional[str] = None


class SubredditInfo(BaseModel):
    """Model for subreddit metadata."""
    name: str
    subscribers: int
    description: str


class Comment(BaseModel):
    """Model for a Reddit comment."""
    id: str
    body: str
    author: str
    score: int
    created_utc: float
    depth: int
    replies: List['Comment'] = Field(default_factory=list)


class SearchResult(BaseModel):
    """Response model for search_reddit tool."""
    results: List[RedditPost]
    count: int


class SubredditPostsResult(BaseModel):
    """Response model for fetch_subreddit_posts tool."""
    posts: List[RedditPost]
    subreddit: SubredditInfo
    count: int


class SubmissionWithCommentsResult(BaseModel):
    """Response model for fetch_submission_with_comments tool."""
    submission: RedditPost
    comments: List[Comment]
    total_comments_fetched: int


# Allow recursive Comment model
Comment.model_rebuild()