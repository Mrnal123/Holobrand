import os
import json
import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock

# Test health check endpoint
def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

# Test file upload endpoint
def test_upload_file_success(client):
    """Test successful file upload"""
    # Create a test image file
    test_file = BytesIO(b'test file content')
    
    # Send the file to the upload endpoint
    response = client.post(
        '/api/upload',
        data={'file': (test_file, 'test_image.jpg')},
        content_type='multipart/form-data'
    )
    
    # Check response
    assert response.status_code == 200
    assert 'message' in response.json
    assert 'filename' in response.json
    assert response.json['message'] == 'File uploaded successfully'
    assert response.json['filename'] == 'test_image.jpg'

def test_upload_file_no_file(client):
    """Test file upload with no file"""
    response = client.post('/api/upload')
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'No file part'

def test_upload_file_empty_filename(client):
    """Test file upload with empty filename"""
    response = client.post(
        '/api/upload',
        data={'file': (BytesIO(b''), '')},
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'No selected file'

# Test generate layout endpoint
@patch('app.layout_generator')
@patch('app.ai_processor')
@patch('app.openai_personalizer')
def test_generate_layout_basic(mock_openai, mock_ai, mock_layout, client):
    """Test basic layout generation without image"""
    # Configure mocks
    mock_layout.generate_layout.return_value = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        }
    }
    
    # Test data
    test_data = {
        'brand_color': '#ff5733',
        'font': 'Roboto',
        'style_prompt': 'modern'
    }
    
    # Send request
    response = client.post(
        '/api/generate-layout',
        json=test_data,
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    assert 'layout' in response.json
    assert response.json['mode'] == '2d'  # Default mode
    
    # Verify mock was called with correct parameters
    mock_layout.generate_layout.assert_called_once_with('#ff5733', 'Roboto', 'modern')

@patch('app.layout_generator')
@patch('app.ai_processor')
@patch('app.openai_personalizer')
@patch('os.path.exists')
def test_generate_layout_with_image(mock_exists, mock_openai, mock_ai, mock_layout, client):
    """Test layout generation with image processing"""
    # Configure mocks
    mock_exists.return_value = True
    mock_layout.generate_layout.return_value = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        }
    }
    mock_ai.process_image.return_value = {
        'dominant_colors': ['#ff5733', '#33ff57'],
        'brightness': 0.7,
        'contrast': 0.5
    }
    mock_ai.analyze_brand_style.return_value = {
        'recommended_style': 'modern',
        'style_scores': {'modern': 0.8, 'elegant': 0.5, 'minimal': 0.3},
        'analysis': {'brightness_level': 'high', 'contrast_level': 'medium'}
    }
    mock_ai.generate_layout_recommendations.return_value = {
        'layout_type': 'asymmetric',
        'spacing': 'medium',
        'animation_type': 'slide'
    }
    
    # Test data
    test_data = {
        'brand_color': '#ff5733',
        'font': 'Roboto',
        'style_prompt': 'modern',
        'image_filename': 'test_image.jpg'
    }
    
    # Send request
    response = client.post(
        '/api/generate-layout',
        json=test_data,
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    assert 'layout' in response.json
    assert 'recommendations' in response.json
    assert 'image_analysis' in response.json
    assert 'brand_analysis' in response.json

# Test 3D preview endpoint
@patch('app.layout_generator')
def test_3d_preview(mock_layout, client):
    """Test 3D preview data generation"""
    # Configure mock
    mock_layout.generate_3d_preview_data.return_value = {
        '3d_elements': [
            {'type': 'cube', 'position': [0, 0, 0], 'color': '#ff5733'},
            {'type': 'sphere', 'position': [1, 1, 1], 'color': '#33ff57'}
        ],
        'camera_position': [5, 5, 5],
        'lighting': 'ambient'
    }
    
    # Test data
    test_data = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        }
    }
    
    # Send request
    response = client.post(
        '/api/3d-preview',
        json=test_data,
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 200
    assert '3d_elements' in response.json
    assert 'camera_position' in response.json
    assert 'lighting' in response.json

# Test GitHub integration endpoints
@patch('app.github_integration')
def test_github_repos_valid_token(mock_github, client):
    """Test GitHub repos endpoint with valid token"""
    # Configure mock
    mock_github.check_token_validity.return_value = True
    mock_github.get_repositories.return_value = [
        {'name': 'repo1', 'full_name': 'user/repo1'},
        {'name': 'repo2', 'full_name': 'user/repo2'}
    ]
    
    # Send request
    response = client.get('/api/github/repos')
    
    # Check response
    assert response.status_code == 200
    assert 'repositories' in response.json
    assert len(response.json['repositories']) == 2

@patch('app.github_integration')
def test_github_repos_invalid_token(mock_github, client):
    """Test GitHub repos endpoint with invalid token"""
    # Configure mock
    mock_github.check_token_validity.return_value = False
    
    # Send request
    response = client.get('/api/github/repos')
    
    # Check response
    assert response.status_code == 401
    assert 'error' in response.json

@patch('app.github_integration')
def test_github_search(mock_github, client):
    """Test GitHub search endpoint"""
    # Configure mock
    mock_github.check_token_validity.return_value = True
    mock_github.search_repositories.return_value = [
        {'name': 'search-repo', 'full_name': 'user/search-repo'}
    ]
    
    # Send request
    response = client.get('/api/github/search?q=test')
    
    # Check response
    assert response.status_code == 200
    assert 'repositories' in response.json
    assert len(response.json['repositories']) == 1

@patch('app.github_integration')
def test_github_search_no_query(mock_github, client):
    """Test GitHub search endpoint without query parameter"""
    # Configure mock
    mock_github.check_token_validity.return_value = True
    
    # Send request
    response = client.get('/api/github/search')
    
    # Check response
    assert response.status_code == 400
    assert 'error' in response.json