import os
import json
import requests
from openai import OpenAI
from image_utils import get_images_by_category

# Load OpenAI API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = None

# Try to initialize OpenAI client
try:
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")

def get_ai_response(messages, prompt=None):
    """Get response from OpenAI"""
    try:
        if not client:
            return generate_fallback_response(messages[-1]["content"] if messages else "")
        
        # Prepare conversation history
        conversation = []
        
        # Add system message if prompt is provided
        if prompt:
            conversation.append({"role": "system", "content": prompt})
        
        # Add user messages
        for msg in messages:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                conversation.append({"role": msg["role"], "content": msg["content"]})
            else:
                # Handle case where message is a string or other format
                content = msg if isinstance(msg, str) else str(msg)
                conversation.append({"role": "user", "content": content})
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return generate_fallback_response(messages[-1]["content"] if messages else "")

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
                "options": ["Show me venues", "Show me dresses", "Show me hairstyles", "Help with wedding party"],
                "state": state
            }
        
        # Get the last message content
        last_message = messages[-1].get("content", "") if isinstance(messages[-1], dict) else ""
        message_lower = last_message.lower() if isinstance(last_message, str) else ""
        
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
            
            # Get AI response
            ai_prompt = "You are a helpful and enthusiastic wedding assistant. Give a short, friendly response about wedding venues. Use emojis and keep it casual."
            ai_response = get_ai_response(messages, ai_prompt)
            
            # Provide venue data
            venue_data = get_images_by_category("venues", style, location)
            
            return {
                "text": ai_response or "Check out these gorgeous venues! Any catching your eye? 👀",
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
            
            # Get AI response
            ai_prompt = "You are a helpful and enthusiastic wedding assistant. Give a short, friendly response about wedding dresses. Use emojis and keep it casual."
            ai_response = get_ai_response(messages, ai_prompt)
            
            # Provide dress data
            dress_data = get_images_by_category("dresses", style)
            
            return {
                "text": ai_response or "These dresses are giving MAIN CHARACTER energy! ✨",
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
            
            # Get AI response
            ai_prompt = "You are a helpful and enthusiastic wedding assistant. Give a short, friendly response about wedding hairstyles. Use emojis and keep it casual."
            ai_response = get_ai_response(messages, ai_prompt)
            
            # Provide hairstyle data
            hairstyle_data = get_images_by_category("hairstyles", style)
            
            return {
                "text": ai_response or "Hair is everything! Check these out! 💇‍♀️",
                "carousel": hairstyle_data.get("carousel"),
                "options": ["Show me venues", "Show me dresses", "Help with wedding party"],
                "state": state
            }
        
        # Check for wedding party help
        elif "wedding party" in message_lower or "party" in message_lower:
            # Get AI response
            ai_prompt = "You are a helpful and enthusiastic wedding assistant. Give advice about wedding party planning and responsibilities. Use emojis and keep it casual."
            ai_response = get_ai_response(messages, ai_prompt)
            
            return {
                "text": ai_response or "Here's who does what in your squad! Delegate like a boss! 💅",
                "options": ["Show me venues", "Show me dresses", "Show me hairstyles"],
                "state": state
            }
        
        # Check for cake-related queries
        elif "cake" in message_lower:
            # Get AI response
            ai_prompt = "You are a helpful and enthusiastic wedding assistant. Give advice about wedding cakes. Use emojis and keep it casual."
            ai_response = get_ai_response(messages, ai_prompt)
            
            # Provide cake data
            cake_data = get_images_by_category("cakes")
            
            return {
                "text": ai_response or "Here are some delicious wedding cake designs! 🎂",
                "carousel": cake_data.get("carousel"),
                "options": ["Show me venues", "Show me dresses", "Show me hairstyles"],
                "state": state
            }
        
        # Check if we've shown enough content to show a soft CTA
        if (state.get("seen_venues") or state.get("seen_dresses") or state.get("seen_hairstyles")) and not state.get("soft_cta_shown"):
            state["soft_cta_shown"] = True
            
            # Get AI response
            ai_prompt = "You are a helpful and enthusiastic wedding assistant. Ask if the user wants to explore more options or get personalized planning help. Use emojis and keep it casual."
            ai_response = get_ai_response(messages, ai_prompt)
            
            return {
                "text": ai_response or "Would you like to explore more options or get personalized wedding planning assistance?",
                "action": "soft_cta",
                "buttons": ["Explore More", "Get Planning Help"],
                "options": ["Explore More", "Get Planning Help"],
                "state": state
            }
        
        # Check if we've shown enough content to show a final CTA
        if state.get("seen_venues") and state.get("seen_dresses") and state.get("seen_hairstyles") and not state.get("cta_shown"):
            state["cta_shown"] = True
            
            # Get AI response
            ai_prompt = "You are a helpful and enthusiastic wedding assistant. Invite the user to join a wedding planning community. Use emojis and keep it casual."
            ai_response = get_ai_response(messages, ai_prompt)
            
            return {
                "text": ai_response or "I've shown you a sneak peek of what I can do! Ready to take your wedding planning to the next level? Over 500 couples have already joined our exclusive wedding planning community!",
                "action": "cta",
                "buttons": ["Join the Waitlist", "Continue Exploring"],
                "options": ["Join the Waitlist", "Continue Exploring"],
                "state": state
            }
        
        # Default response - use OpenAI for conversational responses
        ai_prompt = "You are a helpful and enthusiastic wedding assistant named Snatcha. Keep responses short, friendly, and use emojis. If the user asks about specific wedding topics, provide helpful advice. Always end with a question to keep the conversation going."
        ai_response = get_ai_response(messages, ai_prompt)
        
        return {
            "text": ai_response or generate_fallback_response(message_lower),
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

def generate_fallback_response(message):
    """Generate a conversational response when OpenAI is unavailable."""
    if "hello" in message.lower() or "hi" in message.lower() or "hey" in message.lower():
        return "Hey there! ✨ What can I help you with for your wedding planning journey?"
    
    if "theme" in message.lower() or "style" in message.lower():
        return "Ooh, let's talk aesthetic! ✨ Are you thinking classic elegance, rustic charm, beachy vibes, or something totally unique? I've got ideas for days! 💭"
    
    if "budget" in message.lower() or "cost" in message.lower():
        return "Let's talk budget! 💰 I can help you find options that won't break the bank but still give you that dream wedding vibe. What range are we working with? 💎"
    
    if "date" in message.lower() or "when" in message.lower():
        return "When are you thinking of having the big day? 📅 Summer weddings are gorgeous, but fall has those amazing colors. Winter is magical too! What season speaks to you? 🌸❄️🍂"
    
    # Default response
    return "I'm here to help with your wedding planning journey! What aspect are you most excited about? 💖" 