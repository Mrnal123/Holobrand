import os
import openai
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIPersonalizer:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
    
    def enhance_layout_with_ai(self, layout_data: Dict[str, Any], style_prompt: str, 
                              image_features: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhance layout with AI personalization using OpenAI
        """
        try:
            # Prepare prompt with layout data and style prompt
            prompt = self._prepare_prompt(layout_data, style_prompt, image_features)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a UI/UX expert specializing in eCommerce layouts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract and parse AI suggestions
            ai_suggestions = response.choices[0].message.content
            enhanced_layout = self._parse_ai_suggestions(layout_data, ai_suggestions)
            
            return enhanced_layout
        except Exception as e:
            print(f"Error in OpenAI personalization: {str(e)}")
            # Return original layout if AI enhancement fails
            return layout_data
    
    def _prepare_prompt(self, layout_data: Dict[str, Any], style_prompt: str, 
                       image_features: Dict[str, Any] = None) -> str:
        """
        Prepare prompt for OpenAI with layout data and style information
        """
        base_prompt = f"""Enhance this eCommerce UI layout based on the style: '{style_prompt}'.
        
        Current layout data:
        {layout_data}
        """
        
        if image_features:
            base_prompt += f"""
            
            Product image features:
            - Dominant colors: {', '.join(image_features.get('dominant_colors', []))}
            - Brightness: {image_features.get('brightness', 0)}
            - Contrast: {image_features.get('contrast', 0)}
            """
        
        base_prompt += """
        
        Please provide specific suggestions to enhance this layout in JSON format with the following structure:
        {"suggestions": {"layout": [...], "colors": [...], "typography": [...], "spacing": [...]}}
        """
        
        return base_prompt
    
    def _parse_ai_suggestions(self, original_layout: Dict[str, Any], 
                            ai_suggestions: str) -> Dict[str, Any]:
        """
        Parse AI suggestions and merge with original layout
        """
        enhanced_layout = original_layout.copy()
        
        try:
            # Extract JSON part from the response if it exists
            import json
            import re
            
            # Try to find JSON pattern in the response
            json_match = re.search(r'\{.*\}', ai_suggestions, re.DOTALL)
            if json_match:
                suggestions_json = json.loads(json_match.group(0))
                
                # Add AI suggestions to the layout
                enhanced_layout['ai_suggestions'] = suggestions_json.get('suggestions', {})
            else:
                # If no JSON found, add raw suggestions
                enhanced_layout['ai_suggestions'] = {
                    "raw": ai_suggestions
                }
        except Exception as e:
            print(f"Error parsing AI suggestions: {str(e)}")
            enhanced_layout['ai_suggestions'] = {
                "error": "Failed to parse AI suggestions",
                "raw": ai_suggestions
            }
        
        return enhanced_layout
    
    def generate_style_description(self, style_prompt: str) -> str:
        """
        Generate a detailed style description based on a brief prompt
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a UI/UX design expert."},
                    {"role": "user", "content": f"Describe a {style_prompt} style for an eCommerce website in 3-4 sentences."}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating style description: {str(e)}")
            return f"A {style_prompt} style for eCommerce."