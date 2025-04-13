import pytest
from ai_personalizer import AIPersonalizationEngine

@pytest.fixture
def mock_layout_data():
    """Create mock layout data for testing template-specific styles"""
    return {
        'layout': {
            'sections': ['hero', 'products', 'cta']
        }
    }

def test_elegant_template_styles(mock_layout_data):
    """Test elegant template-specific interaction styles"""
    engine = AIPersonalizationEngine()
    mock_layout_data['template'] = 'elegant'
    
    elements = engine.generate_interactive_elements(mock_layout_data)
    
    # Verify elegant hero style
    hero = next(e for e in elements if e['type'] == 'spotlight')
    assert hero['style'] == 'fade'
    assert hero['z_offset'] == 80
    assert hero['duration_multiplier'] == 1.2
    
    # Verify elegant products style
    products = next(e for e in elements if e['type'] == 'carousel')
    assert products['style'] == 'smooth'
    assert products['z_offset'] == 30
    assert products['spacing'] == 120
    
    # Verify elegant CTA style
    cta = next(e for e in elements if e['type'] == 'button')
    assert cta['style'] == 'floating'
    assert cta['z_offset'] == 50

def test_modern_template_styles(mock_layout_data):
    """Test modern template-specific interaction styles"""
    engine = AIPersonalizationEngine()
    mock_layout_data['template'] = 'modern'
    
    elements = engine.generate_interactive_elements(mock_layout_data)
    
    # Verify modern hero style
    hero = next(e for e in elements if e['type'] == 'spotlight')
    assert hero['style'] == 'dynamic'
    assert hero['z_offset'] == 80
    assert hero['duration_multiplier'] == 1.0
    
    # Verify modern products style
    products = next(e for e in elements if e['type'] == 'carousel')
    assert products['style'] == 'interactive'
    assert products['z_offset'] == 40
    assert products['spacing'] == 100
    
    # Verify modern CTA style
    cta = next(e for e in elements if e['type'] == 'button')
    assert cta['style'] == 'pulse'
    assert cta['z_offset'] == 20

def test_minimal_template_styles(mock_layout_data):
    """Test minimal template-specific interaction styles"""
    engine = AIPersonalizationEngine()
    mock_layout_data['template'] = 'minimal'
    
    elements = engine.generate_interactive_elements(mock_layout_data)
    
    # Verify minimal hero style
    hero = next(e for e in elements if e['type'] == 'spotlight')
    assert hero['style'] == 'simple'
    assert hero['z_offset'] == 60
    assert hero['duration_multiplier'] == 0.8
    
    # Verify minimal products style
    products = next(e for e in elements if e['type'] == 'carousel')
    assert products['style'] == 'basic'
    assert products['z_offset'] == 25
    assert products['spacing'] == 80
    
    # Verify minimal CTA style
    cta = next(e for e in elements if e['type'] == 'button')
    assert cta['style'] == 'clean'
    assert cta['z_offset'] == 35

def test_dynamic_positioning():
    """Test dynamic positioning calculation for sections"""
    engine = AIPersonalizationEngine()
    layout_data = {
        'template': 'modern',
        'layout': {
            'sections': ['hero', 'products', 'cta']
        }
    }
    
    elements = engine.generate_interactive_elements(layout_data)
    
    # Verify positions are calculated correctly
    positions = [e['position'] for e in elements]
    
    # Check that elements have different positions
    assert len(set(str(p) for p in positions)) == len(positions)
    
    # Check that z-positions follow template style
    z_positions = [p['z'] for p in positions]
    assert z_positions[0] >= z_positions[1]  # Hero should be furthest back
    assert z_positions[1] >= z_positions[2]  # Products in middle