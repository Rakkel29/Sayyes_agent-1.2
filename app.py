import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from sayyes_agent import process_message

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