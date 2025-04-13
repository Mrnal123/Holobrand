import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from ai_utils import AIProcessor

# Create a mock image for testing
@pytest.fixture
def mock_image():
    """Create a mock image for testing"""
    # Create a simple 10x10 RGB image with random values
    return np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)

@pytest.fixture
def mock_image_path(tmp_path, mock_image):
    """Create a temporary image file for testing"""
    import cv2
    # Create a temporary directory and file
    test_dir = tmp_path / "test_images"
    test_dir.mkdir()
    test_file = test_dir / "test_image.jpg"
    
    # Save the mock image to the file
    cv2.imwrite(str(test_file), mock_image)
    
    return str(test_file)

def test_init():
    """Test AIProcessor initialization"""
    processor = AIProcessor()
    assert processor.image_size == (512, 512)
    assert 'elegant' in processor.style_features
    assert 'modern' in processor.style_features
    assert 'minimal' in processor.style_features

@patch('cv2.imread')
@patch('cv2.cvtColor')
@patch('cv2.resize')
def test_process_image(mock_resize, mock_cvtcolor, mock_imread, mock_image):
    """Test image processing functionality"""
    # Configure mocks
    mock_imread.return_value = mock_image
    mock_cvtcolor.return_value = mock_image
    mock_resize.return_value = mock_image
    
    processor = AIProcessor()
    # Mock the _extract_dominant_colors method
    processor._extract_dominant_colors = MagicMock(return_value=['#ff0000', '#00ff00', '#0000ff'])
    
    # Process the image
    features = processor.process_image('dummy_path.jpg')
    
    # Verify results
    assert 'dimensions' in features
    assert 'dominant_colors' in features
    assert 'brightness' in features
    assert 'contrast' in features
    assert features['dominant_colors'] == ['#ff0000', '#00ff00', '#0000ff']

def test_extract_dominant_colors(mock_image):
    """Test dominant color extraction"""
    processor = AIProcessor()
    
    # Extract dominant colors
    colors = processor._extract_dominant_colors(mock_image, num_colors=2)
    
    # Verify results
    assert len(colors) == 2
    assert all(color.startswith('#') for color in colors)
    assert all(len(color) == 7 for color in colors)  # #RRGGBB format

def test_analyze_brand_style():
    """Test brand style analysis"""
    processor = AIProcessor()
    
    # Create mock image features
    image_features = {
        'brightness': 200,  # High brightness (0-255)
        'contrast': 50,     # Low contrast (0-255)
        'dominant_colors': ['#ffffff', '#f0f0f0', '#e0e0e0']  # Light colors
    }
    
    # Test with 'elegant' style prompt
    analysis = processor.analyze_brand_style(image_features, 'elegant luxury')
    assert 'recommended_style' in analysis
    assert 'style_scores' in analysis
    assert 'analysis' in analysis
    assert analysis['analysis']['brightness_level'] == 'high'
    assert analysis['analysis']['contrast_level'] == 'low'
    
    # The elegant score should be boosted due to the style prompt
    assert analysis['style_scores']['elegant'] > analysis['style_scores']['modern']
    
    # Test with 'modern' style prompt
    analysis = processor.analyze_brand_style(image_features, 'modern tech')
    assert 'modern' in analysis['style_scores']
    
    # Test with 'minimal' style prompt
    analysis = processor.analyze_brand_style(image_features, 'minimal clean')
    assert 'minimal' in analysis['style_scores']

def test_generate_layout_recommendations():
    """Test layout recommendation generation"""
    processor = AIProcessor()
    
    # Test with 'elegant' style
    brand_analysis = {
        'recommended_style': 'elegant',
        'analysis': {
            'brightness_level': 'high',
            'contrast_level': 'medium'
        }
    }
    
    recommendations = processor.generate_layout_recommendations(brand_analysis)
    assert 'layout_type' in recommendations
    assert 'spacing' in recommendations
    assert 'animation_type' in recommendations
    assert 'suggested_elements' in recommendations
    assert recommendations['layout_type'] == 'centered'
    
    # Test with 'modern' style
    brand_analysis['recommended_style'] = 'modern'
    recommendations = processor.generate_layout_recommendations(brand_analysis)
    assert recommendations['layout_type'] == 'asymmetric'
    
    # Test with 'minimal' style
    brand_analysis['recommended_style'] = 'minimal'
    recommendations = processor.generate_layout_recommendations(brand_analysis)
    assert recommendations['layout_type'] == 'grid'
    assert recommendations['spacing'] == 'large'