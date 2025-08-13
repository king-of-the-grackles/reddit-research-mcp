#!/usr/bin/env python3
"""Simple test to verify the discover_subreddits fix works."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.discover import discover_subreddits
from unittest.mock import Mock

def test_queries_as_json_string():
    """Test that queries parameter accepts JSON string."""
    # Mock Reddit instance
    mock_reddit = Mock()
    mock_subreddit = Mock()
    mock_subreddit.display_name = "dogs"
    mock_subreddit.title = "Dogs"
    mock_subreddit.public_description = "All about dogs"
    mock_subreddit.subscribers = 1000000
    mock_subreddit.over18 = False
    mock_subreddit.id = "test_id"
    mock_subreddit.created_utc = 1234567890
    
    # Mock the search results
    mock_reddit.subreddits.search.return_value = [mock_subreddit]
    
    # Test with JSON string (the problematic case from logs)
    json_string = '["dogs", "dog health", "veterinary", "pet care", "dog allergies"]'
    
    result = discover_subreddits(
        queries=json_string,
        reddit=mock_reddit,
        limit=10,
        include_nsfw=False
    )
    
    # Should return batch results without error
    assert result is not None
    assert "batch_mode" in result
    assert result["batch_mode"] is True
    assert "results" in result
    assert len(result["results"]) == 5  # 5 queries
    
    print("✅ JSON string test passed!")

def test_queries_as_list():
    """Test that queries parameter still works with list."""
    # Mock Reddit instance
    mock_reddit = Mock()
    mock_subreddit = Mock()
    mock_subreddit.display_name = "dogs"
    mock_subreddit.title = "Dogs"  
    mock_subreddit.public_description = "All about dogs"
    mock_subreddit.subscribers = 1000000
    mock_subreddit.over18 = False
    mock_subreddit.id = "test_id"
    mock_subreddit.created_utc = 1234567890
    
    # Mock the search results
    mock_reddit.subreddits.search.return_value = [mock_subreddit]
    
    # Test with list (normal case)
    queries_list = ["dogs", "dog health", "veterinary"]
    
    result = discover_subreddits(
        queries=queries_list,
        reddit=mock_reddit,
        limit=10,
        include_nsfw=False
    )
    
    # Should return batch results without error
    assert result is not None
    assert "batch_mode" in result
    assert result["batch_mode"] is True
    assert "results" in result
    assert len(result["results"]) == 3  # 3 queries
    
    print("✅ List test passed!")

def test_queries_as_single_string():
    """Test that single string query works."""
    # Mock Reddit instance
    mock_reddit = Mock()
    mock_subreddit = Mock()
    mock_subreddit.display_name = "dogs"
    mock_subreddit.title = "Dogs"
    mock_subreddit.public_description = "All about dogs"
    mock_subreddit.subscribers = 1000000
    mock_subreddit.over18 = False
    mock_subreddit.id = "test_id"
    mock_subreddit.created_utc = 1234567890
    
    # Mock the search results
    mock_reddit.subreddits.search.return_value = [mock_subreddit]
    
    # Test with single string (edge case)
    single_query = "dogs"
    
    result = discover_subreddits(
        queries=single_query,
        reddit=mock_reddit,
        limit=10,
        include_nsfw=False
    )
    
    # Should return batch results with 1 query
    assert result is not None
    assert "batch_mode" in result
    assert result["batch_mode"] is True
    assert "results" in result
    assert len(result["results"]) == 1  # 1 query
    
    print("✅ Single string test passed!")

if __name__ == "__main__":
    test_queries_as_json_string()
    test_queries_as_list()
    test_queries_as_single_string()
    print("🎉 All tests passed! The fix is working correctly.")