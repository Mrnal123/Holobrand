# HoloBrand - Multimodal UI Generator for eCommerce

HoloBrand is a hackathon project that generates brand-aligned UI layouts using AI and provides both 2D web previews and immersive 3D visualization through Unreal Engine.

## Features

- Upload product images and specify brand preferences
- AI-powered layout generation with style analysis
- Rule-based and GPT-enhanced layout recommendations
- 2D web preview with responsive layouts
- 3D immersive visualization via Unreal Engine
- Qiskit integration for layout randomization

## Tech Stack

### Backend
- Flask (REST API)
- OpenCV & Pillow (Image Processing)
- OpenAI GPT (Layout Personalization)
- SQLite (Data Storage)
- Qiskit (Quantum Computing Integration)

### Frontend (To be implemented)
- HTML/CSS/JavaScript
- Modern UI Framework
- Responsive Design

### 3D Visualization (To be implemented)
- Unreal Engine 5.3+
- Blueprints
- UMG for UI
- VaRest Plugin

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file with required environment variables:
   ```
   OPENAI_API_KEY=your_api_key_here
   GITHUB_TOKEN=your_github_personal_access_token_here
   ```
5. Run the development server:
   ```bash
   python app.py
   ```

## API Endpoints

### Health Check
- `GET /health`
  - Check if the service is running

### Upload Product Image
- `POST /api/upload`
  - Upload product image file
  - Returns filename and upload status

### Generate Layout
- `POST /api/generate-layout`
  - Request body:
    ```json
    {
        "brand_color": "#FF5733",
        "font": "Arial",
        "style_prompt": "Elegant skincare",
        "preview_mode": "2D"
    }
    ```
  - Returns generated layout configuration

### 3D Preview Data
- `POST /api/3d-preview`
  - Get 3D visualization data for Unreal Engine
  - Returns scene configuration and UI element data

### GitHub Integration
- `GET /api/github/repos`
  - Retrieve repositories for the authenticated user or a specific GitHub user
  - Optional query parameter: `username`

- `GET /api/github/search`
  - Search for GitHub repositories based on a query
  - Required query parameter: `q`

## Project Structure

```
├── app.py              # Main Flask application
├── layout_generator.py # Layout generation logic
├── ai_utils.py         # AI processing utilities
├── requirements.txt    # Python dependencies
├── uploads/           # Uploaded files directory
└── README.md          # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.