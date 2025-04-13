import os
import pytest
import requests
from unittest.mock import patch, MagicMock
from github_utils import GitHubIntegration

@pytest.fixture
def github_integration():
    """Create a GitHubIntegration instance for testing"""
    # Set up environment variable for testing
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"}):
        return GitHubIntegration()

def test_init():
    """Test GitHubIntegration initialization"""
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"}):
        integration = GitHubIntegration()
        assert integration.base_url == "https://api.github.com"
        assert integration.token == "test_token"
        assert integration.headers["Authorization"] == "token test_token"
        assert integration.headers["Accept"] == "application/vnd.github.v3+json"

def test_check_token_validity_valid(github_integration):
    """Test token validity check with valid token"""
    with patch('requests.get') as mock_get:
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Check token validity
        result = github_integration.check_token_validity()
        
        # Verify results
        assert result is True
        mock_get.assert_called_once_with(
            "https://api.github.com/user", 
            headers=github_integration.headers
        )

def test_check_token_validity_invalid(github_integration):
    """Test token validity check with invalid token"""
    with patch('requests.get') as mock_get:
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 401  # Unauthorized
        mock_get.return_value = mock_response
        
        # Check token validity
        result = github_integration.check_token_validity()
        
        # Verify results
        assert result is False

def test_check_token_validity_exception(github_integration):
    """Test token validity check with exception"""
    with patch('requests.get') as mock_get:
        # Configure mock to raise exception
        mock_get.side_effect = Exception("Connection error")
        
        # Check token validity
        result = github_integration.check_token_validity()
        
        # Verify results
        assert result is False

def test_check_token_validity_empty_token():
    """Test token validity check with empty token"""
    with patch.dict(os.environ, {"GITHUB_TOKEN": ""}):
        integration = GitHubIntegration()
        result = integration.check_token_validity()
        assert result is False

def test_check_token_validity_default_token():
    """Test token validity check with default token"""
    with patch.dict(os.environ, {"GITHUB_TOKEN": "your_github_personal_access_token_here"}):
        integration = GitHubIntegration()
        result = integration.check_token_validity()
        assert result is False

def test_get_repositories_authenticated(github_integration):
    """Test getting repositories for authenticated user"""
    with patch('requests.get') as mock_get:
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"name": "repo1", "full_name": "user/repo1"},
            {"name": "repo2", "full_name": "user/repo2"}
        ]
        mock_get.return_value = mock_response
        
        # Get repositories
        repos = github_integration.get_repositories()
        
        # Verify results
        assert len(repos) == 2
        assert repos[0]["name"] == "repo1"
        assert repos[1]["name"] == "repo2"
        mock_get.assert_called_once_with(
            "https://api.github.com/user/repos", 
            headers=github_integration.headers
        )

def test_get_repositories_specific_user(github_integration):
    """Test getting repositories for a specific user"""
    with patch('requests.get') as mock_get:
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"name": "repo1", "full_name": "testuser/repo1"}
        ]
        mock_get.return_value = mock_response
        
        # Get repositories for specific user
        repos = github_integration.get_repositories("testuser")
        
        # Verify results
        assert len(repos) == 1
        assert repos[0]["name"] == "repo1"
        mock_get.assert_called_once_with(
            "https://api.github.com/users/testuser/repos", 
            headers=github_integration.headers
        )

def test_get_repositories_error(github_integration):
    """Test getting repositories with error response"""
    with patch('requests.get') as mock_get:
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 404  # Not found
        mock_get.return_value = mock_response
        
        # Get repositories
        repos = github_integration.get_repositories()
        
        # Verify results
        assert repos == []

def test_get_repositories_exception(github_integration):
    """Test getting repositories with exception"""
    with patch('requests.get') as mock_get:
        # Configure mock to raise exception
        mock_get.side_effect = Exception("Connection error")
        
        # Get repositories
        repos = github_integration.get_repositories()
        
        # Verify results
        assert repos == []

def test_search_repositories(github_integration):
    """Test searching repositories"""
    with patch('requests.get') as mock_get:
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"name": "search-repo1", "full_name": "user/search-repo1"},
                {"name": "search-repo2", "full_name": "user/search-repo2"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Search repositories
        repos = github_integration.search_repositories("test-query")
        
        # Verify results
        assert len(repos) == 2
        assert repos[0]["name"] == "search-repo1"
        assert repos[1]["name"] == "search-repo2"
        mock_get.assert_called_once_with(
            "https://api.github.com/search/repositories?q=test-query", 
            headers=github_integration.headers
        )

def test_search_repositories_error(github_integration):
    """Test searching repositories with error response"""
    with patch('requests.get') as mock_get:
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 422  # Unprocessable entity
        mock_get.return_value = mock_response
        
        # Search repositories
        repos = github_integration.search_repositories("test-query")
        
        # Verify results
        assert repos == []

def test_search_repositories_exception(github_integration):
    """Test searching repositories with exception"""
    with patch('requests.get') as mock_get:
        # Configure mock to raise exception
        mock_get.side_effect = Exception("Connection error")
        
        # Search repositories
        repos = github_integration.search_repositories("test-query")
        
        # Verify results
        assert repos == []