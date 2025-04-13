import os
import pytest
import json
import re
from unittest.mock import patch, MagicMock
from openai_utils import OpenAIPersonalizer

@pytest.fixture
def openai_personalizer():
    """Create an OpenAIPersonalizer instance for testing"""
    # Set up environment variable for testing
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        return OpenAIPersonalizer()

def test_init():
    """Test OpenAIPersonalizer initialization"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        personalizer = OpenAIPersonalizer()
        assert personalizer.model == "gpt-3.5-turbo"

@patch('openai.ChatCompletion.create')
def test_enhance_layout_with_ai_success(mock_openai_create, openai_personalizer):
    """Test successful layout enhancement with OpenAI"""
    # Sample layout data
    layout_data = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        },
        'colors': {
            'primary': '#ff0000',
            'secondary': '#00ff00'
        }
    }
    
    # Configure mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "suggestions": {
            "layout": ["Add a testimonials section", "Use a grid layout for products"],
            "colors": ["Use a darker shade for buttons", "Add a highlight color"],
            "typography": ["Use sans-serif fonts", "Increase heading sizes"],
            "spacing": ["Add more whitespace between sections", "Use consistent padding"]
        }
    })
    mock_openai_create.return_value = mock_response
    
    # Enhance layout
    enhanced_layout = openai_personalizer.enhance_layout_with_ai(layout_data, "modern")
    
    # Verify results
    assert 'ai_suggestions' in enhanced_layout
    assert 'layout' in enhanced_layout['ai_suggestions']
    assert 'colors' in enhanced_layout['ai_suggestions']
    assert 'typography' in enhanced_layout['ai_suggestions']
    assert 'spacing' in enhanced_layout['ai_suggestions']
    assert len(enhanced_layout['ai_suggestions']['layout']) == 2
    
    # Verify OpenAI API was called correctly
    mock_openai_create.assert_called_once()
    args, kwargs = mock_openai_create.call_args
    assert kwargs['model'] == "gpt-3.5-turbo"
    assert len(kwargs['messages']) == 2
    assert kwargs['messages'][0]['role'] == "system"
    assert kwargs['messages'][1]['role'] == "user"
    assert "modern" in kwargs['messages'][1]['content']

@patch('openai.ChatCompletion.create')
def test_enhance_layout_with_ai_with_image_features(mock_openai_create, openai_personalizer):
    """Test layout enhancement with image features"""
    # Sample layout data
    layout_data = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        }
    }
    
    # Sample image features
    image_features = {
        'dominant_colors': ['#ff0000', '#00ff00', '#0000ff'],
        'brightness': 0.7,
        'contrast': 0.5
    }
    
    # Configure mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = json.dumps({
        "suggestions": {
            "layout": ["Use a color-focused layout"],
            "colors": ["Use dominant colors from the image"],
            "typography": ["Use contrasting fonts"],
            "spacing": ["Balance whitespace with color blocks"]
        }
    })
    mock_openai_create.return_value = mock_response
    
    # Enhance layout with image features
    enhanced_layout = openai_personalizer.enhance_layout_with_ai(
        layout_data, "colorful", image_features
    )
    
    # Verify results
    assert 'ai_suggestions' in enhanced_layout
    
    # Verify OpenAI API was called with image features
    mock_openai_create.assert_called_once()
    args, kwargs = mock_openai_create.call_args
    assert "dominant colors" in kwargs['messages'][1]['content'].lower()
    assert "#ff0000" in kwargs['messages'][1]['content']

@patch('openai.ChatCompletion.create')
def test_enhance_layout_with_ai_non_json_response(mock_openai_create, openai_personalizer):
    """Test handling of non-JSON response from OpenAI"""
    # Sample layout data
    layout_data = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        }
    }
    
    # Configure mock response with non-JSON content
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a text response without JSON"
    mock_openai_create.return_value = mock_response
    
    # Enhance layout
    enhanced_layout = openai_personalizer.enhance_layout_with_ai(layout_data, "modern")
    
    # Verify results - should contain raw suggestions
    assert 'ai_suggestions' in enhanced_layout
    assert 'raw' in enhanced_layout['ai_suggestions']
    assert enhanced_layout['ai_suggestions']['raw'] == "This is a text response without JSON"

@patch('openai.ChatCompletion.create')
def test_enhance_layout_with_ai_exception(mock_openai_create, openai_personalizer):
    """Test handling of exceptions during OpenAI API call"""
    # Sample layout data
    layout_data = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        }
    }
    
    # Configure mock to raise exception
    mock_openai_create.side_effect = Exception("API error")
    
    # Enhance layout - should return original layout on error
    enhanced_layout = openai_personalizer.enhance_layout_with_ai(layout_data, "modern")
    
    # Verify results - should return original layout
    assert enhanced_layout == layout_data

@patch('openai.ChatCompletion.create')
def test_generate_style_description(mock_openai_create, openai_personalizer):
    """Test style description generation"""
    # Configure mock response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "A modern, minimalist design with clean lines and bold typography."
    mock_openai_create.return_value = mock_response
    
    # Generate style description
    description = openai_personalizer.generate_style_description("modern minimalist")
    
    # Verify results
    assert description == "A modern, minimalist design with clean lines and bold typography."
    
    # Verify OpenAI API was called correctly
    mock_openai_create.assert_called_once()
    args, kwargs = mock_openai_create.call_args
    assert kwargs['model'] == "gpt-3.5-turbo"
    assert "modern minimalist" in kwargs['messages'][1]['content']

@patch('openai.ChatCompletion.create')
def test_generate_style_description_exception(mock_openai_create, openai_personalizer):
    """Test handling of exceptions during style description generation"""
    # Configure mock to raise exception
    mock_openai_create.side_effect = Exception("API error")
    
    # Generate style description - should return default on error
    description = openai_personalizer.generate_style_description("modern")
    
    # Verify results - should return default description
    assert "style" in description.lower()
    assert "modern" in description.lower()