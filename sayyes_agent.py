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

def process_message(message_data):
    """
    Process a message and return the response.
    
    Args:
        message_data: Dictionary containing messages and state
        
    Returns:
        Dictionary with response text and updated state
    """
    # Extract messages and state from the request
    try:
        messages = message_data.get("messages", [])
        state = message_data.get("state", {})
        
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
                "text": "Hello! I'm your wedding planning assistant. How can I help you today?",
                "state": state
            }
        
        last_message = messages[-1].get("content", "") if isinstance(messages[-1], dict) else ""
        
        print(f"Processing message: {last_message}")
        
        # If LLM is not available, return a fallback response
        if llm is None:
            return {
                "text": "I'm sorry, but I'm having trouble accessing my language model. Please check your API keys and try again.",
                "state": state
            }
        
        # Create message objects for the LLM
        conversation_history = []
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    conversation_history.append(HumanMessage(content=content))
                else:
                    conversation_history.append(AIMessage(content=content))
            else:
                # Handle case where message is a string
                conversation_history.append(HumanMessage(content=str(msg)))
        
        # Prepare system message based on state
        system_content = """
        You are Snatcha, a fun, warm, and helpful AI wedding planning assistant.
        Keep responses short, friendly, and use emojis where appropriate.
        Respond like you're helping a close friend, but stay focused on the task.
        """
        
        system_message = SystemMessage(content=system_content)
        
        # Basic response using LLM
        response = llm.invoke([system_message] + conversation_history)
        response_text = response.content
        
        # Check message for keywords to determine next actions
        message_lower = last_message.lower() if isinstance(last_message, str) else ""
        
        # Check for venue-related queries
        if ("venue" in message_lower or "location" in message_lower) and not state["seen_venues"]:
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
            
            # Get venue images
            venue_data = get_images_by_category("venues", style, location)
            
            if venue_data and "carousel" in venue_data and venue_data["carousel"]["items"]:
                return {
                    "text": f"Here are some beautiful wedding venues that might interest you! {response_text}",
                    "action": "show_carousel",
                    "carousel": venue_data["carousel"],
                    "state": state
                }
        
        # Check for dress-related queries
        elif ("dress" in message_lower or "gown" in message_lower) and not state["seen_dresses"]:
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
            
            # Get dress images
            dress_data = get_images_by_category("dresses", style)
            
            if dress_data and "carousel" in dress_data and dress_data["carousel"]["items"]:
                return {
                    "text": f"Here are some stunning wedding dresses! {response_text}",
                    "action": "show_carousel",
                    "carousel": dress_data["carousel"],
                    "state": state
                }
        
        # Check for hairstyle-related queries
        elif ("hair" in message_lower or "hairstyle" in message_lower) and not state["seen_hairstyles"]:
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
            
            # Get hairstyle images
            hairstyle_data = get_images_by_category("hairstyles", style)
            
            if hairstyle_data and "carousel" in hairstyle_data and hairstyle_data["carousel"]["items"]:
                return {
                    "text": f"Here are some beautiful wedding hairstyles! {response_text}",
                    "action": "show_carousel",
                    "carousel": hairstyle_data["carousel"],
                    "state": state
                }
        
        # Check for cake-related queries
        elif "cake" in message_lower:
            # Get cake images
            cake_data = get_images_by_category("cakes")
            
            if cake_data and "carousel" in cake_data and cake_data["carousel"]["items"]:
                return {
                    "text": f"Here are some delicious wedding cake designs! {response_text}",
                    "action": "show_carousel",
                    "carousel": cake_data["carousel"],
                    "state": state
                }
        
        # Check if we've shown enough content to show a soft CTA
        if (state["seen_venues"] or state["seen_dresses"] or state["seen_hairstyles"]) and not state["soft_cta_shown"]:
            state["soft_cta_shown"] = True
            return {
                "text": f"{response_text}\n\nWould you like to explore more options or get personalized wedding planning assistance?",
                "action": "soft_cta",
                "buttons": ["Explore More", "Get Planning Help"],
                "state": state
            }
        
        # Check if we've shown enough content to show a final CTA
        if state["seen_venues"] and state["seen_dresses"] and state["seen_hairstyles"] and not state["cta_shown"]:
            state["cta_shown"] = True
            return {
                "text": f"{response_text}\n\nI've shown you a sneak peek of what I can do! Ready to take your wedding planning to the next level? Over 500 couples have already joined our exclusive wedding planning community!",
                "action": "cta",
                "buttons": ["Join the Waitlist", "Continue Exploring"],
                "state": state
            }
        
        # Default response
        return {
            "text": response_text,
            "state": state
        }
    
    except Exception as e:
        print(f"Error processing message: {e}")
        return {
            "text": "I'm sorry, but I encountered an error processing your message. Please try again.",
            "state": state if isinstance(state, dict) else {}
        } 