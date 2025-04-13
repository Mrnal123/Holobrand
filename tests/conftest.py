import os
import sys
import pytest
from flask import Flask
from unittest.mock import MagicMock

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from layout_generator import LayoutGenerator
from ai_utils import AIProcessor
from openai_utils import OpenAIPersonalizer
from github_utils import GitHubIntegration

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Set testing configuration
    flask_app.config.update({
        'TESTING': True,
        'UPLOAD_FOLDER': 'tests/test_uploads',
    })
    
    # Ensure test upload directory exists
    os.makedirs(flask_app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    yield flask_app
    
    # Cleanup after tests
    import shutil
    if os.path.exists(flask_app.config['UPLOAD_FOLDER']):
        shutil.rmtree(flask_app.config['UPLOAD_FOLDER'])

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def layout_generator():
    """Create a LayoutGenerator instance for testing"""
    return LayoutGenerator()

@pytest.fixture
def ai_processor():
    """Create an AIProcessor instance for testing"""
    return AIProcessor()

@pytest.fixture
def openai_personalizer():
    """Create a mock OpenAIPersonalizer for testing"""
    mock_personalizer = MagicMock(spec=OpenAIPersonalizer)
    
    # Mock the enhance_layout_with_ai method
    mock_personalizer.enhance_layout_with_ai.return_value = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products', 'testimonials', 'cta'],
        },
        'ai_suggestions': {
            'layout': ['Use a hero section with a large product image'],
            'colors': ['Use complementary colors for call-to-action buttons'],
            'typography': ['Use sans-serif fonts for modern appeal'],
            'spacing': ['Increase spacing between sections for better readability']
        }
    }
    
    # Mock the generate_style_description method
    mock_personalizer.generate_style_description.return_value = "A modern, clean design with emphasis on product visuals."
    
    return mock_personalizer

@pytest.fixture
def github_integration():
    """Create a mock GitHubIntegration for testing"""
    mock_github = MagicMock(spec=GitHubIntegration)
    
    # Mock the check_token_validity method
    mock_github.check_token_validity.return_value = True
    
    # Mock the get_repositories method
    mock_github.get_repositories.return_value = [
        {
            'id': 1,
            'name': 'test-repo',
            'full_name': 'test-user/test-repo',
            'html_url': 'https://github.com/test-user/test-repo',
            'description': 'Test repository',
            'owner': {'login': 'test-user'}
        }
    ]
    
    # Mock the search_repositories method
    mock_github.search_repositories.return_value = [
        {
            'id': 2,
            'name': 'search-result',
            'full_name': 'test-user/search-result',
            'html_url': 'https://github.com/test-user/search-result',
            'description': 'Search result repository',
            'owner': {'login': 'test-user'}
        }
    ]
    
    return mock_github