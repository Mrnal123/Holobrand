import os
import json
import math
from typing import Dict, Any, List, Optional
from openai_utils import OpenAIPersonalizer

class AIPersonalizationEngine:
    """Enhanced AI personalization engine for HoloBrand layouts"""
    
    def __init__(self):
        self.openai_personalizer = OpenAIPersonalizer()
        self.style_mappings = {
            'elegant': ['luxury', 'premium', 'sophisticated', 'high-end', 'classy'],
            'modern': ['contemporary', 'sleek', 'tech', 'innovative', 'cutting-edge'],
            'minimal': ['clean', 'simple', 'uncluttered', 'essential', 'streamlined']
        }
        self.product_categories = [
            'fashion', 'electronics', 'home', 'beauty', 'food', 
            'fitness', 'automotive', 'jewelry', 'furniture', 'art'
        ]
    
    def analyze_product_image(self, image_features: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced analysis on product image features"""
        dominant_colors = image_features.get('dominant_colors', [])
        brightness = image_features.get('brightness', 0)
        contrast = image_features.get('contrast', 0)
        
        # Determine color temperature (warm vs cool)
        color_temp = self._analyze_color_temperature(dominant_colors)
        
        # Determine visual complexity
        complexity = self._calculate_visual_complexity(brightness, contrast)
        
        # Determine suggested product category based on visual features
        suggested_category = self._suggest_product_category(dominant_colors, brightness, contrast)
        
        return {
            'color_temperature': color_temp,
            'visual_complexity': complexity,
            'suggested_category': suggested_category,
            'color_analysis': self._analyze_color_palette(dominant_colors)
        }
    
    def _analyze_color_temperature(self, colors: List[str]) -> str:
        """Analyze if color palette is warm or cool"""
        warm_hues = ['red', 'orange', 'yellow', 'brown']
        cool_hues = ['blue', 'green', 'purple', 'teal']
        
        warm_count = 0
        cool_count = 0
        
        for color in colors:
            # Simple heuristic - red/green balance in hex
            if color.startswith('#') and len(color) == 7:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                
                # Warm colors have more red than blue
                if r > b:
                    warm_count += 1
                else:
                    cool_count += 1
        
        if warm_count > cool_count:
            return 'warm'
        elif cool_count > warm_count:
            return 'cool'
        else:
            return 'neutral'
    
    def _calculate_visual_complexity(self, brightness: float, contrast: float) -> str:
        """Calculate visual complexity based on brightness and contrast"""
        # Normalize values
        brightness_norm = brightness / 255 if brightness > 1 else brightness
        contrast_norm = contrast / 255 if contrast > 1 else contrast
        
        # Calculate complexity score
        complexity_score = (contrast_norm * 0.7) + ((1 - brightness_norm) * 0.3)
        
        if complexity_score < 0.3:
            return 'simple'
        elif complexity_score < 0.6:
            return 'moderate'
        else:
            return 'complex'
    
    def _suggest_product_category(self, colors: List[str], brightness: float, contrast: float) -> str:
        """Suggest product category based on visual features"""
        # This is a simplified heuristic - in a real implementation, this would use ML
        brightness_norm = brightness / 255 if brightness > 1 else brightness
        
        # Simple heuristics for demonstration
        if brightness_norm > 0.7 and self._analyze_color_temperature(colors) == 'cool':
            return 'electronics'
        elif brightness_norm < 0.4 and contrast > 0.6:
            return 'luxury'
        elif self._analyze_color_temperature(colors) == 'warm' and brightness_norm > 0.5:
            return 'fashion'
        else:
            return 'general'
    
    def _analyze_color_palette(self, colors: List[str]) -> Dict[str, Any]:
        """Analyze color palette characteristics"""
        if not colors:
            return {'harmony': 'unknown', 'palette_type': 'unknown'}
        
        # Determine if colors are monochromatic, complementary, etc.
        if len(colors) == 1 or len(set(colors)) == 1:
            palette_type = 'monochromatic'
        elif len(colors) == 2:
            palette_type = 'complementary'
        elif len(colors) == 3:
            palette_type = 'triadic'
        else:
            palette_type = 'diverse'
        
        # Simple harmony check - in reality would be more sophisticated
        harmony = 'harmonious' if palette_type in ['monochromatic', 'complementary'] else 'complex'
        
        return {
            'harmony': harmony,
            'palette_type': palette_type,
            'count': len(colors)
        }
    
    def enhance_3d_layout(self, layout_data: Dict[str, Any], image_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enhance 3D layout based on AI analysis"""
        enhanced_layout = layout_data.copy()
        template = enhanced_layout.get('template', 'modern')
        
        # Apply enhancements based on template and image analysis
        if image_analysis:
            color_temp = image_analysis.get('color_temperature', 'neutral')
            complexity = image_analysis.get('visual_complexity', 'moderate')
            
            # Adjust environment based on color temperature
            if 'environment' in enhanced_layout:
                if color_temp == 'warm':
                    enhanced_layout['environment']['post_processing']['color_grading'] = 'warm'
                elif color_temp == 'cool':
                    enhanced_layout['environment']['post_processing']['color_grading'] = 'cool'
            
            # Adjust camera settings based on visual complexity
            if 'camera' in enhanced_layout:
                if complexity == 'simple':
                    enhanced_layout['camera']['field_of_view'] = 65  # Wider view for simple layouts
                elif complexity == 'complex':
                    enhanced_layout['camera']['field_of_view'] = 55  # Narrower for complex layouts
                    enhanced_layout['camera']['depth_of_field'] = True  # Add depth of field for complex scenes
        
        # Add AI-generated suggestions
        if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_api_key_here":
            try:
                # Get style description from OpenAI
                style_prompt = f"A {template} style 3D layout for e-commerce"
                style_description = self.openai_personalizer.generate_style_description(style_prompt)
                
                # Add to layout metadata
                if 'metadata' in enhanced_layout:
                    enhanced_layout['metadata']['style_description'] = style_description
                    enhanced_layout['metadata']['ai_enhanced'] = True
            except Exception as e:
                print(f"OpenAI enhancement failed: {str(e)}")
        
        return enhanced_layout
    
    def generate_interactive_elements(self, layout_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate interactive elements for 3D layout with dynamic positioning and template-based interactions"""
        if not isinstance(layout_data, dict) or 'layout' not in layout_data or 'sections' not in layout_data['layout']:
            return []
    
        sections = layout_data['layout']['sections']
        template = layout_data.get('template', 'modern')
        
        # Define template-specific interaction styles
        template_styles = {
            'elegant': {
                'hero': {'type': 'spotlight', 'style': 'fade', 'z_offset': 80, 'duration_multiplier': 1.2},
                'products': {'type': 'carousel', 'style': 'smooth', 'z_offset': 30, 'spacing': 120},
                'cta': {'type': 'button', 'style': 'floating', 'z_offset': 50}
            },
            'modern': {
                'hero': {'type': 'spotlight', 'style': 'dynamic', 'z_offset': 80, 'duration_multiplier': 1.0},
                'products': {'type': 'carousel', 'style': 'interactive', 'z_offset': 40, 'spacing': 100},
                'cta': {'type': 'button', 'style': 'pulse', 'z_offset': 20}
            },
            'minimal': {
                'hero': {'type': 'spotlight', 'style': 'simple', 'z_offset': 60, 'duration_multiplier': 0.8},
                'products': {'type': 'carousel', 'style': 'basic', 'z_offset': 25, 'spacing': 80},
                'cta': {'type': 'button', 'style': 'clean', 'z_offset': 35}
            }
        }
        
        style = template_styles.get(template, template_styles['modern'])
        interactive_elements = []
        
        for i, section in enumerate(sections):
            base_position = self._calculate_section_position(i, len(sections), style)
            
            if section == 'hero':
                hero_style = style['hero']
                interactive_elements.append({
                    'id': f'hero_{i}',
                    'type': hero_style['type'],
                    'target': section,
                    'style': hero_style['style'],
                    'z_offset': hero_style['z_offset'],
                    'duration_multiplier': hero_style['duration_multiplier'],
                    'actions': [
                        {'type': 'zoom', 'duration': 1.0 * hero_style['duration_multiplier']},
                        {'type': 'highlight', 'duration': 0.5 * hero_style['duration_multiplier']},
                        {'type': 'parallax', 'intensity': 0.3},
                        {'type': 'show_details', 'content': 'hero_content'}
                    ],
                    'position': {
                        'x': base_position['x'],
                        'y': base_position['y'],
                        'z': hero_style['z_offset']
                    },
                    'animation': {
                        'entry': 'fade_in',
                        'idle': 'float',
                        'exit': 'fade_out'
                    }
                })
            elif section in ['products', 'gallery']:
                product_style = style['products']
                interactive_elements.append({
                    'id': f'{section}_{i}',
                    'type': product_style['type'],
                    'target': section,
                    'style': product_style['style'],
                    'z_offset': product_style['z_offset'],
                    'spacing': product_style['spacing'],
                    'actions': [
                        {'type': 'rotate', 'duration': 1.5},
                        {'type': 'zoom_hover', 'scale': 1.1},
                        {'type': 'show_details', 'content': f'{section}_content'}
                    ],
                    'position': {
                        'x': base_position['x'] + (i * product_style['spacing']),
                        'y': base_position['y'],
                        'z': product_style['z_offset']
                    },
                    'animation': {
                        'entry': 'slide_in',
                        'idle': 'rotate_slow',
                        'exit': 'slide_out'
                    }
                })
            elif section == 'cta':
                cta_style = style['cta']
                interactive_elements.append({
                    'id': f'cta_{i}',
                    'type': cta_style['type'],
                    'target': section,
                    'style': cta_style['style'],
                    'z_offset': cta_style['z_offset'],
                    'actions': [
                        {'type': 'click', 'duration': 0.3},
                        {'type': 'pulse', 'intensity': 0.5},
                        {'type': 'show_details', 'content': 'cta_content'}
                    ],
                    'position': {
                        'x': 0,  # Fixed x position for CTA
                        'y': 150,  # Fixed y position for CTA
                        'z': 40  # Fixed z position for CTA
                    },
                    'animation': {
                        'entry': 'bounce_in',
                        'idle': 'pulse',
                        'exit': 'bounce_out'
                    }
                })
        
        return interactive_elements

    def _calculate_section_position(self, index: int, total_sections: int, style: Dict[str, Any]) -> Dict[str, float]:
        """Calculate base position for a section based on its index and total number of sections"""
        template = style.get('template', 'modern')
        
        if template == 'elegant':
            # Elegant layout uses a curved ascending path
            angle = (index / total_sections) * math.pi
            radius = 150
            return {
                'x': radius * math.cos(angle),
                'y': 80 + (index * 30),  # Higher elevation for elegant feel
                'z': radius * math.sin(angle) * 0.5  # Compressed depth for better visibility
            }
        elif template == 'minimal':
            # Minimal layout uses a grid-like pattern
            grid_size = math.ceil(math.sqrt(total_sections))
            row = index // grid_size
            col = index % grid_size
            spacing = 120
            return {
                'x': (col - grid_size/2) * spacing,
                'y': 50 + (row * spacing/2),
                'z': 0  # Flat layout for minimal design
            }
        else:  # Modern layout (default)
            # Modern layout uses a dynamic spiral pattern
            angle = (index / total_sections) * 2 * math.pi
            radius = 100 + (index * 10)  # Increasing radius for spiral effect
            z_base = radius * math.sin(angle)
            # Adjust z-position to maintain proper layering with template z-offsets
            return {
                'x': 0 if index == 0 else radius * math.cos(angle),  # Hero section at center
                'y': 0 if index == 0 else 60 + (index * 25),
                'z': 70 if index == 0 else z_base * 0.5  # Hero section at z=70
            }
        
        return interactive_elements
    
    def suggest_layout_improvements(self, layout_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest improvements for the layout based on best practices"""
        template = layout_data.get('template', 'modern')
        sections = layout_data.get('layout', {}).get('sections', [])
        
        suggestions = []
        
        # Check for essential sections
        essential_sections = ['hero', 'cta']
        for section in essential_sections:
            if section not in sections:
                suggestions.append({
                    'type': 'layout',
                    'suggestion': f"Add a {section} section for better conversion",
                    'priority': 'high'
                })
        
        # Suggest 3D enhancements based on template
        if template == 'elegant':
            suggestions.extend([
                {
                    'type': '3d',
                    'suggestion': "Add subtle particle effects for luxury feel",
                    'priority': 'medium'
                },
                {
                    'type': '3d',
                    'suggestion': "Increase material reflectivity for premium appearance",
                    'priority': 'medium'
                }
            ])
        elif template == 'modern':
            suggestions.extend([
                {
                    'type': '3d',
                    'suggestion': "Add tech-inspired holographic elements",
                    'priority': 'high'
                },
                {
                    'type': '3d',
                    'suggestion': "Use animated wireframes for background elements",
                    'priority': 'medium'
                }
            ])
        elif template == 'minimal':
            suggestions.extend([
                {
                    'type': '3d',
                    'suggestion': "Simplify materials with flat shading",
                    'priority': 'high'
                },
                {
                    'type': '3d',
                    'suggestion': "Use subtle depth changes instead of complex animations",
                    'priority': 'medium'
                }
            ])
        
        return suggestions