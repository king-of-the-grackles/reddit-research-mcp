import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import get_reddit_client


class TestConfig:
    def test_get_reddit_client_with_env_vars(self, monkeypatch):
        """Test Reddit client creation with environment variables."""
        # Set environment variables
        monkeypatch.setenv("REDDIT_CLIENT_ID", "test_client_id")
        monkeypatch.setenv("REDDIT_CLIENT_SECRET", "test_client_secret")
        monkeypatch.setenv("REDDIT_USER_AGENT", "TestAgent/1.0")
        
        # Mock praw.Reddit to avoid actual API calls
        with patch('src.config.praw.Reddit') as mock_reddit_class:
            mock_reddit_instance = Mock()
            mock_reddit_class.return_value = mock_reddit_instance
            
            # Call the function
            client = get_reddit_client()
            
            # Assert Reddit was initialized with correct parameters
            mock_reddit_class.assert_called_once_with(
                client_id="test_client_id",
                client_secret="test_client_secret",
                user_agent="TestAgent/1.0",
                redirect_uri="http://localhost:8080",
                ratelimit_seconds=300
            )
            
            # Assert read_only mode was set
            assert mock_reddit_instance.read_only == True
            
            # Assert the client is returned
            assert client == mock_reddit_instance
    
    def test_get_reddit_client_with_dotenv(self, monkeypatch):
        """Test Reddit client creation from .env file."""
        # Clear environment variables
        monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
        monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
        monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)
        
        # Mock .env file existence and loading
        # Since user_agent uses the default in line 15, it will be "RedditMCP/1.0"
        # Then when .env loads and user_agent is still None, it gets set from .env
        env_content = {
            "REDDIT_CLIENT_ID": "dotenv_client_id",
            "REDDIT_CLIENT_SECRET": "dotenv_client_secret",
            "REDDIT_USER_AGENT": "DotEnvAgent/1.0"
        }
        
        with patch('src.config.Path.exists', return_value=True), \
             patch('src.config.load_dotenv') as mock_load_dotenv, \
             patch('src.config.os.getenv', side_effect=env_content.get), \
             patch('src.config.praw.Reddit') as mock_reddit_class:
            
            mock_reddit_instance = Mock()
            mock_reddit_class.return_value = mock_reddit_instance
            
            # Call the function
            client = get_reddit_client()
            
            # Assert load_dotenv was called
            mock_load_dotenv.assert_called_once()
            
            # Assert Reddit was initialized with dotenv values
            # Note: user_agent defaults to "RedditMCP/1.0" before checking .env file
            mock_reddit_class.assert_called_once_with(
                client_id="dotenv_client_id",
                client_secret="dotenv_client_secret",
                user_agent="RedditMCP/1.0",  # Default is used because line 15 sets it
                redirect_uri="http://localhost:8080",
                ratelimit_seconds=300
            )
            
            # Assert read_only mode was set
            assert mock_reddit_instance.read_only == True
            
            # Assert the client is returned
            assert client == mock_reddit_instance
    
    def test_get_reddit_client_missing_credentials(self, monkeypatch):
        """Test error when credentials are missing."""
        # Clear all environment variables
        monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
        monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
        monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)
        
        # Mock .env file as non-existent
        with patch('src.config.Path.exists', return_value=False):
            # Assert ValueError is raised with helpful message
            with pytest.raises(ValueError) as exc_info:
                get_reddit_client()
            
            error_message = str(exc_info.value)
            assert "Reddit API credentials not found" in error_message
            assert "REDDIT_CLIENT_ID" in error_message
            assert "REDDIT_CLIENT_SECRET" in error_message
            assert ".env file" in error_message
    
    def test_get_reddit_client_default_user_agent(self, monkeypatch):
        """Test default user agent is applied when not specified."""
        # Set credentials but not user agent
        monkeypatch.setenv("REDDIT_CLIENT_ID", "test_client_id")
        monkeypatch.setenv("REDDIT_CLIENT_SECRET", "test_client_secret")
        monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)
        
        # Mock praw.Reddit
        with patch('src.config.praw.Reddit') as mock_reddit_class:
            mock_reddit_instance = Mock()
            mock_reddit_class.return_value = mock_reddit_instance
            
            # Call the function
            client = get_reddit_client()
            
            # Assert default user agent "RedditMCP/1.0" is used
            mock_reddit_class.assert_called_once_with(
                client_id="test_client_id",
                client_secret="test_client_secret",
                user_agent="RedditMCP/1.0",  # Default value
                redirect_uri="http://localhost:8080",
                ratelimit_seconds=300
            )
            
            # Assert read_only mode was set
            assert mock_reddit_instance.read_only == True
            
            # Assert the client is returned
            assert client == mock_reddit_instance
    
    def test_get_reddit_client_partial_dotenv_credentials(self, monkeypatch):
        """Test that .env file is used when only partial credentials in environment."""
        # Set only client_id in environment
        monkeypatch.setenv("REDDIT_CLIENT_ID", "env_client_id")
        monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
        monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)
        
        # Mock .env file with complete credentials
        env_content = {
            "REDDIT_CLIENT_ID": "dotenv_client_id",
            "REDDIT_CLIENT_SECRET": "dotenv_client_secret",
            "REDDIT_USER_AGENT": "DotEnvAgent/1.0"
        }
        
        with patch('src.config.Path.exists', return_value=True), \
             patch('src.config.load_dotenv') as mock_load_dotenv, \
             patch('src.config.os.getenv', side_effect=env_content.get), \
             patch('src.config.praw.Reddit') as mock_reddit_class:
            
            mock_reddit_instance = Mock()
            mock_reddit_class.return_value = mock_reddit_instance
            
            # Call the function
            client = get_reddit_client()
            
            # Assert load_dotenv was called since client_secret was missing
            mock_load_dotenv.assert_called_once()
            
            # Assert Reddit was initialized with dotenv values
            # Note: user_agent defaults to "RedditMCP/1.0" because line 15 sets it
            mock_reddit_class.assert_called_once_with(
                client_id="dotenv_client_id",
                client_secret="dotenv_client_secret",
                user_agent="RedditMCP/1.0",  # Default is used from line 15
                redirect_uri="http://localhost:8080",
                ratelimit_seconds=300
            )