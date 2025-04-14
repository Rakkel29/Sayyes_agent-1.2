import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import json
from image_utils import get_images_by_category

# Load environment variables
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY environment variable is not set")

# Initialize LLM (if API key is available)
try:
    llm = ChatOpenAI(
        model="gpt-4", 
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )
except Exception as e:
    print(f"Warning: Could not initialize LLM: {e}")
    llm = None

def get_wedding_images(category: str, style=None, location=None) -> str:
    """
    Get wedding images for a specific category.
    
    Args:
        category: Type of images (venues, dresses, hairstyles, cakes, etc.)
        style: Optional style descriptor (rustic, modern, bohemian, etc.)
        location: Optional location specification
        
    Returns:
        JSON string with image URLs and descriptions
    """
    try:
        # Get images from blob storage using the function from image_utils
        images = get_images_by_category(category, style, location)
        
        # If no images found, return empty list
        if not images:
            return json.dumps([])
        
        return json.dumps(images)
    except Exception as e:
        print(f"Error in get_wedding_images: {e}")
        return json.dumps([])

def process_message(data):
    """
    Process a message and return the response.
    
    Args:
        data: Dictionary containing messages and state
        
    Returns:
        Dictionary with response text and updated state
    """
    try:
        # Extract messages and state from the request
        messages = data.get("messages", [])
        state = data.get("state", {})
        
        # Initialize state if empty
        if not state:
            state = {
                "seen_venues": False,
                "seen_dresses": False,
                "seen_hairstyles": False,
                "cta_shown": False,
                "soft_cta_shown": False
            }
        
        # Get the last message from the user
        if not messages or len(messages) == 0:
            return {
                "text": "Hey! I'm your AI wedding planner. Ready to explore your dream day?",
                "options": ["Show me venues", "Show me dresses", "Help with wedding party"],
                "state": state
            }
        
        # Get the last message content
        last_message = messages[-1].get("content", "") if isinstance(messages[-1], dict) else ""
        
        # Check message for keywords to determine next actions
        message_lower = last_message.lower()
        
        # Check for venue-related queries
        if ("venue" in message_lower or "location" in message_lower) and not state.get("seen_venues", False):
            state["seen_venues"] = True
            
            # Extract style and location if present
            style = None
            location = None
            
            if "rustic" in message_lower:
                style = "rustic"
            elif "modern" in message_lower:
                style = "modern"
            elif "elegant" in message_lower or "luxury" in message_lower:
                style = "luxury"
            elif "bohemian" in message_lower or "boho" in message_lower:
                style = "bohemian"
            
            # Extract location - basic implementation
            if "in " in message_lower:
                location = message_lower.split("in ")[-1].strip()
                location = location.split()[0]  # Take the first word after "in"
            
            # Provide venue data
            venue_data = get_images_by_category("venues", style, location)
            
            return {
                "text": "Check out these gorgeous venues! Any catching your eye? 👀",
                "carousel": venue_data.get("carousel"),
                "options": ["Show me dresses", "Show me hairstyles", "Help with wedding party"],
                "state": state
            }
        
        # Check for dress-related queries
        elif ("dress" in message_lower or "gown" in message_lower) and not state.get("seen_dresses", False):
            state["seen_dresses"] = True
            
            # Extract style if present
            style = None
            if "rustic" in message_lower:
                style = "rustic"
            elif "modern" in message_lower:
                style = "modern"
            elif "elegant" in message_lower or "luxury" in message_lower:
                style = "luxury"
            elif "bohemian" in message_lower or "boho" in message_lower:
                style = "bohemian"
            
            # Provide dress data
            dress_data = get_images_by_category("dresses", style)
            
            return {
                "text": "These dresses are giving MAIN CHARACTER energy! ✨",
                "carousel": dress_data.get("carousel"),
                "options": ["Show me venues", "Show me hairstyles", "Help with wedding party"],
                "state": state
            }
        
        # Check for hairstyle-related queries
        elif ("hair" in message_lower or "hairstyle" in message_lower) and not state.get("seen_hairstyles", False):
            state["seen_hairstyles"] = True
            
            # Extract style if present
            style = None
            if "rustic" in message_lower:
                style = "rustic"
            elif "modern" in message_lower:
                style = "modern"
            elif "elegant" in message_lower or "luxury" in message_lower:
                style = "luxury"
            elif "bohemian" in message_lower or "boho" in message_lower:
                style = "bohemian"
            
            # Provide hairstyle data
            hairstyle_data = get_images_by_category("hairstyles", style)
            
            return {
                "text": "Hair is everything! Check these out! 💇‍♀️",
                "carousel": hairstyle_data.get("carousel"),
                "options": ["Show me venues", "Show me dresses", "Help with wedding party"],
                "state": state
            }
        
        # Check for wedding party help
        elif "wedding party" in message_lower or "party" in message_lower:
            return {
                "text": "Here's who does what in your squad! Delegate like a boss! 💅",
                "options": ["Show me venues", "Show me dresses", "Show me hairstyles"],
                "state": state
            }
        
        # Check for cake-related queries
        elif "cake" in message_lower:
            # Provide cake data
            cake_data = get_images_by_category("cakes")
            
            return {
                "text": "Here are some delicious wedding cake designs! 🎂",
                "carousel": cake_data.get("carousel"),
                "options": ["Show me venues", "Show me dresses", "Show me hairstyles"],
                "state": state
            }
        
        # Check if we've shown enough content to show a soft CTA
        if (state.get("seen_venues") or state.get("seen_dresses") or state.get("seen_hairstyles")) and not state.get("soft_cta_shown"):
            state["soft_cta_shown"] = True
            return {
                "text": "Would you like to explore more options or get personalized wedding planning assistance?",
                "action": "soft_cta",
                "buttons": ["Explore More", "Get Planning Help"],
                "options": ["Explore More", "Get Planning Help"],
                "state": state
            }
        
        # Check if we've shown enough content to show a final CTA
        if state.get("seen_venues") and state.get("seen_dresses") and state.get("seen_hairstyles") and not state.get("cta_shown"):
            state["cta_shown"] = True
            return {
                "text": "I've shown you a sneak peek of what I can do! Ready to take your wedding planning to the next level? Over 500 couples have already joined our exclusive wedding planning community!",
                "action": "cta",
                "buttons": ["Join the Waitlist", "Continue Exploring"],
                "options": ["Join the Waitlist", "Continue Exploring"],
                "state": state
            }
        
        # Default response
        return {
            "text": generate_response(message_lower),
            "options": get_options_based_on_state(state),
            "state": state
        }
    
    except Exception as e:
        print(f"Error processing message: {e}")
        return {
            "text": "I'm sorry, but I encountered an error processing your message. Please try again.",
            "state": state if isinstance(state, dict) else {}
        }

def get_options_based_on_state(state):
    """Get appropriate options based on the current state."""
    if state.get("seen_venues"):
        return ["Show me dresses", "Show me hairstyles", "Help with wedding party"]
    elif state.get("seen_dresses"):
        return ["Show me venues", "Show me hairstyles", "Help with wedding party"]
    elif state.get("seen_hairstyles"):
        return ["Show me venues", "Show me dresses", "Help with wedding party"]
    else:
        return ["Show me venues", "Show me dresses", "Show me hairstyles", "Help with wedding party"]

def generate_response(message):
    """Generate a conversational response."""
    if "hello" in message or "hi" in message or "hey" in message:
        return "Hey there! ✨ What can I help you with for your wedding planning journey?"
    
    if "theme" in message or "style" in message:
        return "Ooh, let's talk aesthetic! ✨ Are you thinking classic elegance, rustic charm, beachy vibes, or something totally unique? I've got ideas for days! 💭"
    
    if "budget" in message or "cost" in message:
        return "Let's talk budget! 💰 I can help you find options that won't break the bank but still give you that dream wedding vibe. What range are we working with? 💎"
    
    if "date" in message or "when" in message:
        return "When are you thinking of having the big day? 📅 Summer weddings are gorgeous, but fall has those amazing colors. Winter is magical too! What season speaks to you? 🌸❄️🍂"
    
    # Default response
    return "I'm here to help with your wedding planning journey! What aspect are you most excited about? 💖" 