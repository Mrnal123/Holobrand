import pytest
from ai_personalizer import AIPersonalizationEngine

@pytest.fixture
def mock_layout_data():
    """Create mock layout data for testing interactive elements"""
    return {
        'template': 'modern',
        'layout': {
            'sections': ['hero', 'products', 'gallery', 'cta']
        }
    }

def test_generate_interactive_elements(mock_layout_data):
    """Test generation of interactive elements for 3D layout"""
    engine = AIPersonalizationEngine()
    
    # Generate interactive elements
    elements = engine.generate_interactive_elements(mock_layout_data)
    
    # Verify the number of elements matches sections
    assert len(elements) == len(mock_layout_data['layout']['sections'])
    
    # Test hero section element
    hero_element = next(e for e in elements if e['type'] == 'spotlight')
    assert hero_element['target'] == 'hero'
    assert len(hero_element['actions']) == 4
    assert hero_element['position'] == {'x': 0, 'y': 0, 'z': 80}
    
    # Test products/gallery section element
    carousel_element = next(e for e in elements if e['type'] == 'carousel')
    assert carousel_element['target'] in ['products', 'gallery']
    assert len(carousel_element['actions']) == 3
    assert all(key in carousel_element['position'] for key in ['x', 'y', 'z'])
    
    # Test CTA section element
    cta_element = next(e for e in elements if e['id'].startswith('cta'))
    assert cta_element['type'] == 'button'
    assert len(cta_element['actions']) == 3
    assert cta_element['position'] == {'x': 0, 'y': 150, 'z': 40}

def test_generate_interactive_elements_empty_layout():
    """Test handling of empty layout data"""
    engine = AIPersonalizationEngine()
    empty_layout = {'template': 'modern', 'layout': {'sections': []}}
    
    elements = engine.generate_interactive_elements(empty_layout)
    assert len(elements) == 0

def test_generate_interactive_elements_missing_layout():
    """Test handling of missing layout data"""
    engine = AIPersonalizationEngine()
    invalid_layout = {'template': 'modern'}
    
    elements = engine.generate_interactive_elements(invalid_layout)
    assert len(elements) == 0