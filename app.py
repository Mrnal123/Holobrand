from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from PIL import Image
import io
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import base64
import subprocess

# Import custom modules
from layout_generator import LayoutGenerator
from ai_utils import AIProcessor
from openai_utils import OpenAIPersonalizer
from github_utils import GitHubIntegration

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize layout generator and AI processor
layout_generator = LayoutGenerator()
ai_processor = AIProcessor()
openai_personalizer = OpenAIPersonalizer()
github_integration = GitHubIntegration()

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})




# Upload endpoint for product images
@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the post request has the file part
        if 'image' not in request.files and 'file' not in request.files:
            return jsonify({'error': 'No file uploaded. Please provide an image file.'}), 400
        
        # Try both 'image' and 'file' fields
        file = request.files.get('image') or request.files.get('file')
        if not file or file.filename == '':
            return jsonify({'error': 'No selected file. Please choose an image to upload.'}), 400

        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({
                'error': 'Invalid file type. Allowed types: PNG, JPG, JPEG, GIF, WEBP'
            }), 400

        # Validate file size (max 16MB)
        if len(file.read()) > 16 * 1024 * 1024:  # 16MB in bytes
            return jsonify({'error': 'File too large. Maximum size is 16MB'}), 400
        file.seek(0)  # Reset file pointer after reading

        # Validate image can be opened
        try:
            img = Image.open(file)
            img.verify()  # Verify it's actually an image
            file.seek(0)  # Reset file pointer after verification
        except Exception:
            return jsonify({'error': 'Invalid image file. Please upload a valid image.'}), 400

        # Save the file in the images subdirectory
        filename = secure_filename(file.filename)
        images_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir, exist_ok=True)
        filepath = os.path.join(images_dir, filename)
        file.save(filepath)

        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'file_size': os.path.getsize(filepath),
            'file_type': file.content_type
        })
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

# Generate layout endpoint
@app.route('/api/generate-layout', methods=['POST'])
def generate_layout():
    try:
        global latest_generated_layout
        
        # Check if the request is form data or JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data
            brand_color = request.form.get('brand_color', '#000000')
            font = request.form.get('font', 'Arial')
            style_prompt = request.form.get('style_prompt', 'modern')
            preview_mode = request.form.get('preview_mode', '2d')
            
            # Handle image upload
            image_filename = None
            if 'image' in request.files and request.files['image'].filename:
                file = request.files['image']
                filename = secure_filename(file.filename)
                images_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
                if not os.path.exists(images_dir):
                    os.makedirs(images_dir, exist_ok=True)
                filepath = os.path.join(images_dir, filename)
                file.save(filepath)
                image_filename = filename
        else:
            # Handle JSON data
            data = request.get_json()
            brand_color = data.get('brand_color', '#000000')
            font = data.get('font', 'Arial')
            style_prompt = data.get('style_prompt', 'modern')
            preview_mode = data.get('preview_mode', '2d')
            image_filename = data.get('image_filename')
        
        # Process image if provided
        image_features = {}
        brand_analysis = {}
        if image_filename:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            if os.path.exists(image_path):
                image_features = ai_processor.process_image(image_path)
                brand_analysis = ai_processor.analyze_brand_style(image_features, style_prompt)
        
        # Generate layout based on selected template style
        layout = layout_generator.generate_layout(brand_color, font, style_prompt)
        latest_generated_layout = layout

        return jsonify(layout)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Remove the duplicate generate_ui endpoint
# Keep only this version
@app.route('/generate-ui', methods=['POST'])
def generate_ui():
    try:
        # Get form data
        image = request.files.get('image')
        color = request.form.get('color')
        font = request.form.get('font')
        prompt = request.form.get('prompt')
        mode = request.form.get('mode')
        
        # Validate inputs
        if not image:
            return jsonify({'status': 'error', 'message': 'No image provided'}), 400
            
        # Save the uploaded image
        filename = secure_filename(image.filename)
        images_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
        os.makedirs(images_dir, exist_ok=True)
        image_path = os.path.join(images_dir, filename)
        image.save(image_path)
        
        # Generate layout using the layout generator
        layout = layout_generator.generate_layout(color, font, prompt)
        
        return jsonify({
            'status': 'generated',
            'message': 'UI generated successfully',
            'layout': layout,
            'image_path': image_path,
            'color': color,
            'font': font,
            'prompt': prompt,
            'mode': mode
        })
        
    except Exception as e:
        app.logger.error(f'Error in generate_ui: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Update the 3D preview endpoint to fix the duplicate code block
@app.route('/api/3d-preview', methods=['POST'])
def get_3d_preview():
    try:
        data = request.get_json()
        layout_data = data.get('layout', {})
        
        # Process image if provided
        image_filename = data.get('image_filename')
        if image_filename:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images', image_filename)
            if os.path.exists(image_path):
                image_features = ai_processor.process_image(image_path)
                brand_analysis = ai_processor.analyze_brand_style(image_features, layout_data.get('template', 'modern'))
                layout_data['image_analysis'] = image_features
                layout_data['brand_analysis'] = brand_analysis

        # Ensure colors are initialized
        if 'colors' not in layout_data:
            layout_data['colors'] = {
                'primary': '#2196F3',
                'secondary': '#FF4081',
                'accent': '#00BCD4',
                'background': '#FFFFFF'
            }

        # Path to Unreal Engine executable
        unreal_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'unreal_assets', 'Brand_Visualizer', 'HolobrandViewer.exe')
        
        # Generate preview URL with layout data
        preview_url = f"holobrand://{base64.b64encode(json.dumps(layout_data).encode()).decode()}"
        
        # Launch Unreal Engine viewer with the data
        if os.path.exists(unreal_path):
            try:
                subprocess.Popen([unreal_path, preview_url])
                return jsonify({
                    'status': 'success',
                    'message': 'Launching 3D preview...',
                    'preview_url': preview_url,
                    'layout_data': layout_data
                })
            except subprocess.SubprocessError as e:
                app.logger.error(f'Failed to launch Unreal Engine viewer: {str(e)}')
                return jsonify({
                    'error': 'Failed to launch 3D preview',
                    'details': str(e)
                }), 500
        else:
            app.logger.error(f'Unreal Engine viewer not found at: {unreal_path}')
            return jsonify({
                'error': 'Unreal Engine viewer not found',
                'path': unreal_path
            }), 404
            
    except Exception as e:
        app.logger.error(f'Error in 3D preview: {str(e)}')
        return jsonify({'error': str(e)}), 500

# GitHub integration endpoints
@app.route('/api/github/repos', methods=['GET'])
def get_github_repos():
    try:
        # Check if GitHub token is valid
        if not github_integration.check_token_validity():
            return jsonify({
                'error': 'Invalid GitHub token. Please set a valid GITHUB_TOKEN in your .env file.'
            }), 401
        
        # Get username from query parameter (optional)
        username = request.args.get('username')
        
        # Get repositories
        repos = github_integration.get_repositories(username)
        
        return jsonify({
            'repositories': repos
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/search', methods=['GET'])
def search_github_repos():
    try:
        # Check if GitHub token is valid
        if not github_integration.check_token_validity():
            return jsonify({
                'error': 'Invalid GitHub token. Please set a valid GITHUB_TOKEN in your .env file.'
            }), 401
        
        # Get search query from query parameter
        query = request.args.get('q')
        if not query:
            return jsonify({
                'error': 'Search query parameter "q" is required'
            }), 400
        
        # Search repositories
        repos = github_integration.search_repositories(query)
        
        return jsonify({
            'repositories': repos
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve frontend files
@app.route('/')
def index():
    return send_from_directory('Holobrand frontend', 'Index (2).html')

# Add the generate-ui endpoint to handle frontend requests
@app.route('/preview')
def preview():
    # Get the layout data from session storage or use default values
    layout_data = request.args.get('layout')
    if layout_data:
        try:
            layout = json.loads(base64.b64decode(layout_data).decode())
        except (json.JSONDecodeError, base64.binascii.Error):
            layout = {
                'colors': {
                    'primary': '#ddcdd2',
                    'secondary': '#2232dd',
                    'accent': '#b0a100',
                    'background': '#f2f0da'
                },
                'typography': {
                    'primary_font': 'Playfair Display',
                    'body_font': 'Arial',
                    'heading_font': 'Playfair Display'
                }
            }
    else:
        layout = {
            'colors': {
                'primary': '#ddcdd2',
                'secondary': '#2232dd',
                'accent': '#b0a100',
                'background': '#f2f0da'
            },
            'typography': {
                'primary_font': 'Playfair Display',
                'body_font': 'Arial',
                'heading_font': 'Playfair Display'
            }
        }
    return render_template('preview.html', layout=layout)


@app.route('/<path:path>')
def serve_static(path):
    # First try to serve from Holobrand frontend folder
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Holobrand frontend')
    if os.path.exists(os.path.join(frontend_path, path)):
        return send_from_directory('Holobrand frontend', path)
    # Fall back to static folder for other assets
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)