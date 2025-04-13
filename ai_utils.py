import os
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List, Tuple
import json

class AIProcessor:
    def __init__(self):
        self.image_size = (512, 512)
        self.style_features = {
            'elegant': ['symmetry', 'minimal', 'luxury'],
            'modern': ['asymmetric', 'bold', 'dynamic'],
            'minimal': ['clean', 'simple', 'spacious']
        }

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Process uploaded product image and extract features"""
        try:
            # Read and preprocess image
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, self.image_size)

            # Extract basic image features
            features = {
                'dimensions': image.shape,
                'dominant_colors': self._extract_dominant_colors(image),
                'brightness': np.mean(image),
                'contrast': np.std(image)
            }

            return features
        except Exception as e:
            raise Exception(f'Error processing image: {str(e)}')

    def _extract_dominant_colors(self, image: np.ndarray, num_colors: int = 3) -> List[str]:
        """Extract dominant colors from image"""
        pixels = image.reshape(-1, 3)
        pixels = np.float32(pixels)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, num_colors, None, criteria, 10, flags)

        _, counts = np.unique(labels, return_counts=True)
        colors = palette[np.argsort(-counts)]

        return [f'#{int(r):02x}{int(g):02x}{int(b):02x}' for r, g, b in colors]

    def analyze_brand_style(self, image_features: Dict[str, Any], style_prompt: str) -> Dict[str, Any]:
        """Analyze brand style based on image features and style prompt"""
        # Basic style analysis based on image features
        brightness_score = image_features['brightness'] / 255
        contrast_score = image_features['contrast'] / 255

        style_scores = {
            'elegant': brightness_score * 0.7 + contrast_score * 0.3,
            'modern': contrast_score * 0.6 + brightness_score * 0.4,
            'minimal': (1 - contrast_score) * 0.8 + brightness_score * 0.2
        }

        # Adjust scores based on style prompt
        prompt_lower = style_prompt.lower()
        for style, keywords in self.style_features.items():
            if any(keyword in prompt_lower for keyword in keywords):
                style_scores[style] += 0.3

        # Get recommended style
        recommended_style = max(style_scores.items(), key=lambda x: x[1])[0]

        return {
            'recommended_style': recommended_style,
            'style_scores': style_scores,
            'analysis': {
                'brightness_level': 'high' if brightness_score > 0.6 else 'medium' if brightness_score > 0.4 else 'low',
                'contrast_level': 'high' if contrast_score > 0.6 else 'medium' if contrast_score > 0.4 else 'low'
            }
        }

    def generate_layout_recommendations(self, brand_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate layout recommendations based on brand analysis"""
        style = brand_analysis['recommended_style']
        brightness = brand_analysis['analysis']['brightness_level']
        contrast = brand_analysis['analysis']['contrast_level']

        recommendations = {
            'layout_type': 'centered' if style == 'elegant' else 'asymmetric' if style == 'modern' else 'grid',
            'spacing': 'large' if style == 'minimal' else 'medium',
            'animation_type': 'fade' if style == 'elegant' else 'slide' if style == 'modern' else 'none',
            'suggested_elements': [
                'hero_section',
                'product_showcase',
                'features_grid',
                'call_to_action'
            ]
        }

        return recommendations