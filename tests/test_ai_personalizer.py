import pytest
from unittest.mock import patch, MagicMock
from ai_personalizer import AIPersonalizationEngine

@pytest.fixture
def mock_layout_data():
    """Create mock layout data for testing"""
    return {
        'template': 'modern',
        'environment': {
            'post_processing': {
                'color_grading': 'neutral'
            }
        },
        'camera': {
            'field_of_view': 70,
            'depth_of_field': False
        },
        'metadata': {}
    }

@pytest.fixture
def mock_image_analysis():
    """Create mock image analysis data for testing"""
    return {
        'color_temperature': 'warm',
        'visual_complexity': 'moderate',
        'suggested_category': 'fashion',
        'color_analysis': {
            'harmony': 'harmonious',
            'palette_type': 'complementary',
            'count': 2
        }
    }

def test_init():
    """Test AIPersonalizationEngine initialization"""
    engine = AIPersonalizationEngine()
    assert hasattr(engine, 'openai_personalizer')
    assert 'elegant' in engine.style_mappings
    assert 'modern' in engine.style_mappings
    assert 'minimal' in engine.style_mappings
    assert len(engine.product_categories) > 0

def test_analyze_product_image():
    """Test product image analysis"""
    engine = AIPersonalizationEngine()
    
    # Test with mock image features
    image_features = {
        'dominant_colors': ['#ff0000', '#00ff00'],
        'brightness': 200,
        'contrast': 50
    }
    
    analysis = engine.analyze_product_image(image_features)
    assert 'color_temperature' in analysis
    assert 'visual_complexity' in analysis
    assert 'suggested_category' in analysis
    assert 'color_analysis' in analysis

def test_analyze_color_temperature():
    """Test color temperature analysis"""
    engine = AIPersonalizationEngine()
    
    # Test warm colors
    warm_colors = ['#ff0000', '#ff8800']  # Red and orange
    assert engine._analyze_color_temperature(warm_colors) == 'warm'
    
    # Test cool colors
    cool_colors = ['#0000ff', '#00ff00']  # Blue and green
    assert engine._analyze_color_temperature(cool_colors) == 'cool'
    
    # Test neutral colors
    neutral_colors = ['#ff0000', '#0000ff']  # Equal warm and cool
    assert engine._analyze_color_temperature(neutral_colors) == 'neutral'

def test_calculate_visual_complexity():
    """Test visual complexity calculation"""
    engine = AIPersonalizationEngine()
    
    # Test simple complexity
    assert engine._calculate_visual_complexity(200, 30) == 'simple'
    
    # Test moderate complexity
    assert engine._calculate_visual_complexity(150, 100) == 'moderate'
    
    # Test high complexity
    assert engine._calculate_visual_complexity(50, 200) == 'complex'

def test_enhance_3d_layout(mock_layout_data, mock_image_analysis):
    """Test 3D layout enhancement"""
    engine = AIPersonalizationEngine()
    
    # Test without OpenAI integration
    enhanced_layout = engine.enhance_3d_layout(mock_layout_data, mock_image_analysis)
    assert enhanced_layout['environment']['post_processing']['color_grading'] == 'warm'
    assert enhanced_layout['camera']['field_of_view'] == 70
    
    # Test with complex visual analysis
    mock_image_analysis['visual_complexity'] = 'complex'
    enhanced_layout = engine.enhance_3d_layout(mock_layout_data, mock_image_analysis)
    assert enhanced_layout['camera']['depth_of_field'] is True
    assert enhanced_layout['camera']['field_of_view'] == 55

def test_generate_interactive_elements():
    """Test interactive elements generation"""
    engine = AIPersonalizationEngine()
    
    layout_data = {
        'layout': {
            'sections': ['hero', 'products', 'gallery', 'cta']
        },
        'template': 'modern'
    }
    
    elements = engine.generate_interactive_elements(layout_data)
    assert len(elements) > 0
    
    # Verify hero section elements
    hero_elements = [e for e in elements if 'hero' in e['id']]
    assert len(hero_elements) > 0
    assert hero_elements[0]['type'] == 'spotlight'
    
    # Verify product/gallery elements
    carousel_elements = [e for e in elements if e['type'] == 'carousel']
    assert len(carousel_elements) > 0

def test_suggest_layout_improvements():
    """Test layout improvement suggestions"""
    engine = AIPersonalizationEngine()
    
    layout_data = {
        'template': 'modern',
        'layout': {
            'sections': ['hero', 'products'],
            'spacing': 'md'
        }
    }
    
    suggestions = engine.suggest_layout_improvements(layout_data)
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    assert all(isinstance(s, dict) for s in suggestions)