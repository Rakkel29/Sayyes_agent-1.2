from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests from Vercel

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        user_message = data.get('message', '')
        stage = data.get('stage', 'initial_greeting')
        user_name = data.get('user_name', '')
        preferences = data.get('preferences', {})

        # Simple response logic (replace with your AI logic if needed)
        response = {
            "description": f"Hi {user_name or 'there'}! I'm here to help with your wedding planning. What would you like to do?",
            "stage": "main_options",
            "options": ["Show me venues", "Show me dresses", "Show me hairstyles", "Show me wedding cakes", "Help with wedding party"]
        }

        # Handle specific user messages
        if "venue" in user_message.lower():
            response = {
                "description": f"Let's find the perfect spot for your big day, {user_name or 'sweetie'}! Here are some gorgeous venues in Austin: 🌟",
                "stage": "venues_path",
                "options": [
                    "Show me more venues",
                    "Show me dresses",
                    "Show me hairstyles",
                    "Show me wedding cakes",
                    "Help with wedding party"
                ]
            }
        elif "dress" in user_message.lower():
            response = {
                "description": f"Let's find the dress of your dreams, {user_name or 'sweetie'}! Here are some stunning wedding dresses: 👗",
                "stage": "dresses_path",
                "options": [
                    "Show me more dresses",
                    "Show me venues",
                    "Show me hairstyles",
                    "Show me wedding cakes",
                    "Help with wedding party"
                ]
            }
        elif "hair" in user_message.lower():
            response = {
                "description": f"Let's find the perfect hairstyle for your big day, {user_name or 'sweetie'}! Here are some gorgeous options: 💇‍♀️",
                "stage": "hairstyles_path",
                "options": [
                    "Show me more hairstyles",
                    "Show me venues",
                    "Show me dresses",
                    "Show me wedding cakes",
                    "Help with wedding party"
                ]
            }
        elif "cake" in user_message.lower():
            response = {
                "description": f"Let's find a delicious cake for your celebration, {user_name or 'sweetie'}! Here are some beautiful wedding cakes: 🎂",
                "stage": "wedding_cakes_path",
                "options": [
                    "Show me more cakes",
                    "Show me venues",
                    "Show me dresses",
                    "Show me hairstyles",
                    "Help with wedding party"
                ]
            }
        elif "party" in user_message.lower() or "help" in user_message.lower():
            response = {
                "description": f"Let's get your wedding party organized, {user_name or 'sweetie'}! Here's how we can manage tasks: 👥",
                "stage": "wedding_party_path",
                "partyTasks": {
                    "Assign Tasks": {
                        "Best Person": ["Plan bachelor/bachelorette party", "Give a toast at the reception"],
                        "Maid of Honor": ["Help with dress shopping", "Assist with wedding day prep"],
                        "Groomsmen": ["Assist with setup", "Help with transportation"],
                        "Bridesmaids": ["Help with decorations", "Support the bride emotionally"]
                    },
                    "Track Progress": {
                        "Best Person": ["Party planning in progress", "Toast prepared"],
                        "Maid of Honor": ["Dress shopping scheduled", "Prep checklist ready"],
                        "Groomsmen": ["Setup confirmed", "Transportation arranged"],
                        "Bridesmaids": ["Decorations in progress", "Support ongoing"]
                    }
                },
                "options": [
                    "Assign more tasks",
                    "Track progress",
                    "Show me venues",
                    "Show me dresses",
                    "Show me hairstyles",
                    "Show me wedding cakes"
                ]
            }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # Get port from environment variable or default to 5001 (Render typically uses 10000)
    port = int(os.environ.get('PORT', 5001))
    app.run(host="0.0.0.0", port=port)