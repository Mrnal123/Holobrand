import pytest
from layout_generator import LayoutGenerator

def test_analyze_style_prompt():
    """Test style prompt analysis"""
    generator = LayoutGenerator()
    
    # Test elegant style detection
    assert generator.analyze_style_prompt('elegant design') == 'elegant'
    assert generator.analyze_style_prompt('luxury brand') == 'elegant'
    
    # Test modern style detection
    assert generator.analyze_style_prompt('modern UI') == 'modern'
    assert generator.analyze_style_prompt('tech startup') == 'modern'
    
    # Test default to minimal
    assert generator.analyze_style_prompt('simple clean') == 'minimal'

def test_generate_color_palette():
    """Test color palette generation"""
    generator = LayoutGenerator()
    
    # Test with black color
    palette = generator.generate_color_palette('#000000')
    assert 'primary' in palette
    assert 'secondary' in palette
    assert 'accent' in palette
    assert 'background' in palette
    assert palette['primary'] == '#000000'
    
    # Test with red color
    palette = generator.generate_color_palette('#ff0000')
    assert palette['primary'] == '#ff0000'
    assert palette['secondary'] == '#00ffff'  # Complementary to red is cyan
    
    # Test with invalid color (should use fallback)
    palette = generator.generate_color_palette('invalid')
    assert 'primary' in palette
    assert 'secondary' in palette

def test_create_layout_structure():
    """Test layout structure creation"""
    generator = LayoutGenerator()
    
    # Test elegant template
    layout = generator.create_layout_structure('elegant')
    assert 'layout' in layout
    assert layout['layout']['spacing'] == 'lg'
    assert layout['layout']['alignment'] == 'center'
    assert 'sections' in layout['layout']
    assert 'animations' in layout['layout']
    
    # Test modern template
    layout = generator.create_layout_structure('modern')
    assert layout['layout']['spacing'] == 'md'
    assert layout['layout']['alignment'] == 'start'
    
    # Test minimal template
    layout = generator.create_layout_structure('minimal')
    assert layout['layout']['spacing'] == 'sm'
    assert layout['layout']['alignment'] == 'center'

def test_generate_layout():
    """Test complete layout generation"""
    generator = LayoutGenerator()
    
    # Test with minimal parameters
    layout = generator.generate_layout('#ff0000', 'Arial', 'modern')
    assert 'layout' in layout
    assert 'colors' in layout
    assert 'typography' in layout
    
    # Verify color palette
    assert layout['colors']['primary'] == '#ff0000'
    
    # Verify typography
    assert layout['typography']['primary_font'] == 'Arial'
    
    # Test with different style
    layout = generator.generate_layout('#00ff00', 'Roboto', 'elegant')
    assert layout['layout']['alignment'] == 'center'  # Elegant uses center alignment

def test_generate_3d_preview_data():
    """Test 3D preview data generation"""
    generator = LayoutGenerator()
    
    # Create a sample layout
    layout_data = {
        'layout': {
            'spacing': 'md',
            'alignment': 'center',
            'sections': ['hero', 'products']
        },
        'colors': {
            'primary': '#ff0000',
            'secondary': '#00ff00',
            'accent': '#0000ff',
            'background': '#ffffff'
        }
    }
    
    # Generate 3D preview data
    preview_data = generator.generate_3d_preview_data(layout_data)
    
    # Verify structure
    assert '3d_elements' in preview_data
    assert 'camera_position' in preview_data
    assert 'lighting' in preview_data
    
    # Verify elements
    assert len(preview_data['3d_elements']) > 0
    assert 'type' in preview_data['3d_elements'][0]
    assert 'position' in preview_data['3d_elements'][0]
    assert 'color' in preview_data['3d_elements'][0]