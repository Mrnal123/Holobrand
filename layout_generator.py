import random
from typing import Dict, Any, List, Optional
import json
import colorsys
from datetime import datetime

# Try to import AI personalizer
try:
    from ai_personalizer import AIPersonalizationEngine
    AI_PERSONALIZER_AVAILABLE = True
except ImportError:
    AI_PERSONALIZER_AVAILABLE = False

# Qiskit not available in this implementation
QISKIT_AVAILABLE = False

class LayoutGenerator:
    def __init__(self):
        # Initialize AI personalizer if available
        self.ai_personalizer = AIPersonalizationEngine() if AI_PERSONALIZER_AVAILABLE else None
        
        self.layout_templates = {
            'elegant': {
                'spacing': 'lg',
                'alignment': 'center',
                'sections': ['hero', 'features', 'gallery', 'cta'],
                'animations': ['fade', 'slide']
            },
            'modern': {
                'spacing': 'md',
                'alignment': 'start',
                'sections': ['hero', 'products', 'testimonials', 'contact'],
                'animations': ['scale', 'rotate']
            },
            'minimal': {
                'spacing': 'sm',
                'alignment': 'center',
                'sections': ['hero', 'showcase', 'about', 'cta'],
                'animations': ['fade']
            }
        }

    def analyze_style_prompt(self, prompt: str) -> str:
        """Analyze style prompt to determine the best template"""
        prompt = prompt.lower()
        if 'elegant' in prompt or 'luxury' in prompt:
            return 'elegant'
        elif 'modern' in prompt or 'tech' in prompt:
            return 'modern'
        else:
            return 'minimal'

    def generate_color_palette(self, brand_color: str) -> Dict[str, str]:
        """Generate a complementary color palette based on brand color"""
        # Convert hex to RGB
        brand_color = brand_color.lstrip('#')
        try:
            r, g, b = tuple(int(brand_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Generate complementary color (opposite on color wheel)
            comp_r, comp_g, comp_b = 255 - r, 255 - g, 255 - b
            complementary = f'#{comp_r:02x}{comp_g:02x}{comp_b:02x}'
            
            # Generate accent color (adjust saturation and brightness)
            import colorsys
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            s = min(1.0, s * 1.5)  # Increase saturation
            v = min(1.0, v * 0.8)  # Slightly darker
            accent_r, accent_g, accent_b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]
            accent = f'#{accent_r:02x}{accent_g:02x}{accent_b:02x}'
            
            # Generate background color (light version of primary)
            bg_h, bg_s, bg_v = h, 0.1, 0.95  # Low saturation, high value
            bg_r, bg_g, bg_b = [int(c * 255) for c in colorsys.hsv_to_rgb(bg_h, bg_s, bg_v)]
            background = f'#{bg_r:02x}{bg_g:02x}{bg_b:02x}'
            
            return {
                'primary': f'#{brand_color}',
                'secondary': complementary,
                'accent': accent,
                'background': background
            }
        except Exception as e:
            # Fallback to default palette if color processing fails
            return {
                'primary': f'#{brand_color}' if brand_color else '#000000',
                'secondary': '#ffffff',
                'accent': '#4a90e2',
                'background': '#f5f5f5'
            }

    def create_layout_structure(self, template_name: str) -> Dict[str, Any]:
        """Create basic layout structure based on template"""
        template = self.layout_templates[template_name]
        return {
            'layout': {
                'spacing': template['spacing'],
                'alignment': template['alignment'],
                'sections': template['sections'],
                'animations': template['animations']
            }
        }

    def _quantum_randomize(self, options: List[Any]) -> Any:
        """
        Simulates quantum randomization using classical random
        In a real implementation, this would use Qiskit for true quantum randomization
        """
        if not options:
            return None
            
        # Use classical randomization
        return random.choice(options)
    
    def generate_layout(self, brand_color: str, font: str, style_prompt: str) -> Dict[str, Any]:
        """Generate a complete layout based on brand color, font and style prompt"""
        try:
            # Analyze style prompt to determine template
            template_name = self.analyze_style_prompt(style_prompt)
            
            # Generate color palette
            color_palette = self.generate_color_palette(brand_color)
            
            # Get template data
            template = self.layout_templates[template_name]
            
            # Use quantum randomization for layout elements
            animations = template.get('animations', [])
            selected_animation = self._quantum_randomize(animations) if animations else None
            
            # Randomize section order while keeping hero at the top
            sections = template.get('sections', [])
            if 'hero' in sections:
                sections.remove('hero')
                randomized_sections = ['hero'] + [self._quantum_randomize(sections) for _ in range(min(3, len(sections)))] 
            else:
                randomized_sections = [self._quantum_randomize(sections) for _ in range(min(4, len(sections)))]
            
            # Create final layout
            layout = {
                'template': template_name,
                'colors': color_palette,
                'typography': {
                    'primary_font': font,
                    'heading_font': font,
                    'body_font': 'Arial'  # Default body font
                },
                'layout': {
                    'spacing': template.get('spacing', 'md'),
                    'alignment': template.get('alignment', 'center'),
                    'sections': randomized_sections,
                    'animations': [selected_animation] if selected_animation else []
                },
                'quantum_enhanced': QISKIT_AVAILABLE
            }

            return layout
        except Exception as e:
            raise Exception(f"Layout generation failed: {str(e)}")

    def generate_3d_preview_data(self, layout: Dict[str, Any], image_features: Optional[Dict[str, Any]] = None, brand_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate 3D preview data for Unreal Engine with AI personalization"""
        # Create default 3D elements based on layout sections
        elements = []
        sections = layout.get('layout', {}).get('sections', [])
        colors = layout.get('colors', {})
        template = layout.get('template', 'modern')
        animations = layout.get('layout', {}).get('animations', [])
        
        # Define section-specific 3D properties
        section_properties = {
            'hero': {
                'type': 'banner',
                'position': {'x': 0, 'y': 0, 'z': 50},
                'color': colors.get('accent', '#0000ff'),
                'scale': 1.2,
                'rotation': {'pitch': 0, 'yaw': 0, 'roll': 0},
                'material': {
                    'roughness': 0.2,
                    'metallic': 0.8,
                    'emissive': 0.1
                },
                'interactive': True,
                'animation': 'float'
            },
            'features': {
                'type': 'panel_group',
                'position': {'x': 100, 'y': 50, 'z': 30},
                'color': colors.get('primary', '#000000'),
                'scale': 0.9,
                'rotation': {'pitch': 15, 'yaw': 0, 'roll': 0},
                'material': {
                    'roughness': 0.5,
                    'metallic': 0.3,
                    'emissive': 0
                },
                'interactive': True,
                'animation': 'rotate'
            },
            'gallery': {
                'type': 'carousel',
                'position': {'x': -100, 'y': 50, 'z': 20},
                'color': colors.get('secondary', '#ffffff'),
                'scale': 1.0,
                'rotation': {'pitch': 0, 'yaw': 30, 'roll': 0},
                'material': {
                    'roughness': 0.3,
                    'metallic': 0.2,
                    'emissive': 0
                },
                'interactive': True,
                'animation': 'slide'
            },
            'products': {
                'type': 'grid',
                'position': {'x': 0, 'y': 100, 'z': 0},
                'color': colors.get('secondary', '#ffffff'),
                'scale': 1.0,
                'rotation': {'pitch': 0, 'yaw': 0, 'roll': 0},
                'material': {
                    'roughness': 0.4,
                    'metallic': 0.5,
                    'emissive': 0
                },
                'interactive': True,
                'animation': 'scale'
            },
            'testimonials': {
                'type': 'quote_cards',
                'position': {'x': 150, 'y': -50, 'z': 10},
                'color': colors.get('background', '#f5f5f5'),
                'scale': 0.8,
                'rotation': {'pitch': 0, 'yaw': -15, 'roll': 0},
                'material': {
                    'roughness': 0.7,
                    'metallic': 0.1,
                    'emissive': 0
                },
                'interactive': True,
                'animation': 'fade'
            },
            'cta': {
                'type': 'button',
                'position': {'x': 0, 'y': 150, 'z': 40},
                'color': colors.get('accent', '#0000ff'),
                'scale': 1.1,
                'rotation': {'pitch': 0, 'yaw': 0, 'roll': 0},
                'material': {
                    'roughness': 0.1,
                    'metallic': 0.9,
                    'emissive': 0.3
                },
                'interactive': True,
                'animation': 'pulse'
            },
            'about': {
                'type': 'text_panel',
                'position': {'x': -150, 'y': -50, 'z': 10},
                'color': colors.get('primary', '#000000'),
                'scale': 0.9,
                'rotation': {'pitch': 0, 'yaw': 15, 'roll': 0},
                'material': {
                    'roughness': 0.6,
                    'metallic': 0.2,
                    'emissive': 0
                },
                'interactive': False,
                'animation': 'fade'
            },
            'contact': {
                'type': 'form',
                'position': {'x': 50, 'y': 150, 'z': 10},
                'color': colors.get('background', '#f5f5f5'),
                'scale': 0.9,
                'rotation': {'pitch': 0, 'yaw': 0, 'roll': 0},
                'material': {
                    'roughness': 0.5,
                    'metallic': 0.3,
                    'emissive': 0
                },
                'interactive': True,
                'animation': 'slide'
            },
            'showcase': {
                'type': 'showcase',
                'position': {'x': 0, 'y': -100, 'z': 20},
                'color': colors.get('secondary', '#ffffff'),
                'scale': 1.2,
                'rotation': {'pitch': 0, 'yaw': 0, 'roll': 0},
                'material': {
                    'roughness': 0.3,
                    'metallic': 0.7,
                    'emissive': 0.1
                },
                'interactive': True,
                'animation': 'rotate'
            }
        }
        
        # Generate a 3D element for each section with enhanced properties
        for i, section in enumerate(sections):
            # Get default properties for this section type or use generic defaults
            props = section_properties.get(section, {
                'type': section,
                'position': {'x': i * 100, 'y': 0, 'z': 0},
                'color': colors.get('primary', '#000000'),
                'scale': 1.0,
                'rotation': {'pitch': 0, 'yaw': 0, 'roll': 0},
                'material': {
                    'roughness': 0.5,
                    'metallic': 0.5,
                    'emissive': 0
                },
                'interactive': False,
                'animation': 'none'
            })
            
            # Add camera position for backward compatibility
            camera_pos = {'x': 0, 'y': -200, 'z': 100}
            props['camera_position'] = camera_pos
            
            # Adjust position based on template and section order
            if template == 'elegant':
                # Elegant template has more vertical arrangement
                props['position']['y'] = i * 80
                props['position']['z'] += 10
            elif template == 'minimal':
                # Minimal template has a more compact arrangement
                props['position']['x'] = i * 70
                props['position']['y'] = i * 20
            
            # Add element with all properties
            elements.append({
                'type': props['type'],
                'position': props['position'],
                'color': props['color'],
                'scale': props['scale'],
                'rotation': props['rotation'],
                'material': props['material'],
                'interactive': props['interactive'],
                'animation': props['animation']
            })
        
        # Determine camera settings based on template
        camera_settings = {
            'elegant': {
                'position': {'x': 0, 'y': -250, 'z': 150},
                'rotation': {'pitch': -15, 'yaw': 0, 'roll': 0},
                'field_of_view': 60,
                'depth_of_field': True
            },
            'modern': {
                'position': {'x': 100, 'y': -200, 'z': 100},
                'rotation': {'pitch': -10, 'yaw': -15, 'roll': 0},
                'field_of_view': 75,
                'depth_of_field': False
            },
            'minimal': {
                'position': {'x': 0, 'y': -180, 'z': 80},
                'rotation': {'pitch': -5, 'yaw': 0, 'roll': 0},
                'field_of_view': 65,
                'depth_of_field': True
            }
        }.get(template, {
            'position': {'x': 0, 'y': -200, 'z': 100},
            'rotation': {'pitch': -10, 'yaw': 0, 'roll': 0},
            'field_of_view': 70,
            'depth_of_field': False
        })
        
        # Determine environment settings based on template
        environment_settings = {
            'elegant': {
                'type': 'studio',
                'ambient_light': 0.3,
                'skylight_intensity': 1.2,
                'reflections': True,
                'post_processing': {
                    'bloom': 0.3,
                    'ambient_occlusion': 0.5,
                    'color_grading': 'warm'
                }
            },
            'modern': {
                'type': 'tech_showroom',
                'ambient_light': 0.2,
                'skylight_intensity': 1.0,
                'reflections': True,
                'post_processing': {
                    'bloom': 0.5,
                    'ambient_occlusion': 0.3,
                    'color_grading': 'cool'
                }
            },
            'minimal': {
                'type': 'neutral',
                'ambient_light': 0.4,
                'skylight_intensity': 0.8,
                'reflections': False,
                'post_processing': {
                    'bloom': 0.1,
                    'ambient_occlusion': 0.2,
                    'color_grading': 'neutral'
                }
            }
        }.get(template, {
            'type': 'showroom',
            'ambient_light': 0.3,
            'skylight_intensity': 1.0,
            'reflections': True,
            'post_processing': {
                'bloom': 0.3,
                'ambient_occlusion': 0.3,
                'color_grading': 'neutral'
            }
        })
        
        # Create interactive elements based on layout
        interactive_elements = []
        for i, section in enumerate(sections):
            if section_properties.get(section, {}).get('interactive', False):
                interactive_elements.append({
                    'id': f'{section}_{i}',
                    'type': 'clickable',
                    'target_element': section,
                    'actions': [
                        {
                            'type': 'highlight',
                            'duration': 0.5,
                            'intensity': 1.2
                        },
                        {
                            'type': 'zoom',
                            'target': section,
                            'duration': 1.0
                        }
                    ]
                })
        
        # Create base 3D preview data
        preview_data = {
            '3d_elements': elements,
            'camera': camera_settings,
            'camera_position': camera_settings['position'],  # Ensure camera_position is at root level
            'lighting': {
                'main_light': {
                    'type': 'directional',
                    'intensity': 1.2,
                    'color': layout['colors']['primary'],
                    'direction': {'x': -0.5, 'y': -0.7, 'z': -0.5}
                },
                'fill_light': {
                    'type': 'point',
                    'intensity': 0.7,
                    'color': layout['colors']['secondary'],
                    'position': {'x': 200, 'y': 100, 'z': 150},
                    'attenuation': 1.5
                },
                'ambient': environment_settings['ambient_light']
            },
            'environment': environment_settings,
            'interactive_elements': interactive_elements,
            'animations': {
                'camera_path': [
                    {
                        'position': camera_settings['position'],
                        'rotation': camera_settings['rotation'],
                        'time': 0
                    },
                    {
                        'position': {
                            'x': camera_settings['position']['x'] + 50,
                            'y': camera_settings['position']['y'] - 50,
                            'z': camera_settings['position']['z'] + 20
                        },
                        'rotation': {
                            'pitch': camera_settings['rotation']['pitch'] - 5,
                            'yaw': camera_settings['rotation']['yaw'] + 10,
                            'roll': 0
                        },
                        'time': 5
                    },
                    {
                        'position': camera_settings['position'],
                        'rotation': camera_settings['rotation'],
                        'time': 10
                    }
                ],
                'element_animations': {
                    'type': animations[0] if animations else 'none',
                    'duration': 1.5,
                    'loop': True,
                    'ease': 'cubic-bezier(0.42, 0, 0.58, 1)'
                }
            },
            'ui_elements': layout,
            'metadata': {
                'version': '2.0',
                'template': template,
                'quantum_enhanced': QISKIT_AVAILABLE,
                'generated_timestamp': self._get_timestamp()
            }
        }
        
        # Apply AI personalization if available
        if self.ai_personalizer and AI_PERSONALIZER_AVAILABLE:
            try:
                # Process image analysis if provided
                if image_features:
                    image_analysis = self.ai_personalizer.analyze_product_image(image_features)
                    preview_data['metadata']['image_analysis'] = image_analysis
                    
                    # Enhance 3D layout with AI personalization
                    preview_data = self.ai_personalizer.enhance_3d_layout(preview_data, image_analysis)
                    
                    # Generate additional interactive elements
                    ai_interactive_elements = self.ai_personalizer.generate_interactive_elements(layout)
                    preview_data['interactive_elements'].extend(ai_interactive_elements)
                    
                    # Get layout improvement suggestions
                    suggestions = self.ai_personalizer.suggest_layout_improvements(layout)
                    preview_data['ai_suggestions'] = suggestions
                    
                    # Mark as AI enhanced
                    preview_data['metadata']['ai_enhanced'] = True
            except Exception as e:
                print(f"AI personalization failed: {str(e)}")
                # Continue with standard preview data if AI enhancement fails
        
        return preview_data
        
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()