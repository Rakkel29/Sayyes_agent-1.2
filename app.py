import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from sayyes_agent import process_message
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow preflight requests explicitly
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Origin"]
    }
})

# Get port from environment variable or default to 8080
port = int(os.environ.get('PORT', 8080))

# Base URL for blob storage
BASE_URL = "https://cmonwuzihtvua2sq.public.blob.vercel-storage.com"

# Image lists matching your uploaded files
dress_images = [
    f"{BASE_URL}/dresses/wedding_dress_mermaid_1.png",
    f"{BASE_URL}/dresses/wedding_dress_aline_2.png",
    f"{BASE_URL}/dresses/wedding_dress_white_3.png",
    f"{BASE_URL}/dresses/wedding_dress_diamond_4.png"
]
hairstyle_images = [
    f"{BASE_URL}/hairstyles/hairstyle_bridal_1.png",
    f"{BASE_URL}/hairstyles/hairstyle_high_bun_2.png",
    f"{BASE_URL}/hairstyles/hairstyle_quinceanera_3.png",
    f"{BASE_URL}/hairstyles/hairstyle_prom_half_up_4.png"
]
venue_images = [
    f"{BASE_URL}/wedding_venues/venue_modern_1.png",
    f"{BASE_URL}/wedding_venues/venue_rustic_2.png",
    f"{BASE_URL}/wedding_venues/venue_elegant_3.png",
    f"{BASE_URL}/wedding_venues/venue_luxurious_4.png"
]
cake_images = [
    f"{BASE_URL}/cakes/cake_floral_1.png",
    f"{BASE_URL}/cakes/cake_modern_2.png",
    f"{BASE_URL}/cakes/cake_vintage_3.png",
    f"{BASE_URL}/cakes/cake_rustic_4.png"
]

# Track the last used image index for rotation
image_indices = {
    'dresses': 0,
    'hairstyles': 0,
    'venues': 0,
    'cakes': 0
}

def get_next_image(category, images):
    global image_indices
    image_indices[category] = (image_indices[category] + 1) % len(images)
    return images[image_indices[category]]

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """
    Endpoint to handle chat requests from the frontend.
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response
    
    try:
        # Log request headers for debugging
        logger.info(f"Request headers: {dict(request.headers)}")
        
        data = request.get_json()
        if not data:
            logger.warning("No data provided in request")
            return jsonify({"error": "No data provided"}), 400

        # Log incoming request
        logger.info(f"Received chat request: {data}")
        
        # Process the message
        result = process_message(data)
        
        # Log the response
        logger.info(f"Sending response: {result}")
        
        # Return the result
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "chat_available": True,
        "version": "1.0.0"
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "status": "SayYes Agent API is running",
        "chat_available": True,
        "environment": "production",
        "endpoints": ["/api/chat", "/api/health"]
    }), 200

if __name__ == '__main__':
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 