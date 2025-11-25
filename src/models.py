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


# Feed API Models

class FeedAnalysis(BaseModel):
    """Analysis data for feed."""
    description: str = Field(..., min_length=10, max_length=1000)
    audience_personas: List[str] = Field(..., min_length=1, max_length=10)
    keywords: List[str] = Field(..., min_length=1, max_length=50)


class SubredditOption(BaseModel):
    """Subreddit option for feed."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=1000)
    subscribers: int = Field(..., ge=0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class FeedCreate(BaseModel):
    """Request model for creating a feed."""
    name: str = Field(..., min_length=1, max_length=255)
    website_url: Optional[str] = None
    analysis: Optional[FeedAnalysis] = None
    selected_subreddits: List[SubredditOption] = Field(..., min_length=1)


class FeedUpdate(BaseModel):
    """Request model for updating a feed (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    website_url: Optional[str] = None
    analysis: Optional[FeedAnalysis] = None
    selected_subreddits: Optional[List[SubredditOption]] = Field(None, min_length=1)


class Feed(BaseModel):
    """Response model for a feed."""
    id: str
    user_id: str
    name: str
    website_url: Optional[str] = None
    analysis: Optional[FeedAnalysis] = None
    selected_subreddits: List[SubredditOption]
    created_at: datetime
    updated_at: datetime


class FeedListResponse(BaseModel):
    """Response model for listing feeds."""
    feeds: List[Feed]
    total: int
    limit: int
    offset: int


class FeedDeleteResponse(BaseModel):
    """Response model for deleting a feed."""
    success: bool
    message: str


class FeedConfig(BaseModel):
    """Response model for feed configuration."""
    profile_id: str
    profile_name: str
    subreddits: List[str]
    show_nsfw: bool
    has_subreddits: bool