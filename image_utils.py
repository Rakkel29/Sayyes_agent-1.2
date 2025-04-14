import os
from dotenv import load_dotenv
from urllib.parse import quote
from typing import List, Dict, Optional
import json

# Load environment variables
load_dotenv()

# Get Vercel Project ID from environment variables
VERCEL_PROJECT_ID = os.environ.get('VERCEL_PROJECT_ID', 'sayyes')

def clean_title(name: str) -> str:
    """Clean and format a title from a filename."""
    return name.split("/")[-1].replace("_", " ").split(".")[0].title()

def clean_description(description: str) -> str:
    """
    Clean and standardize a description string.
    
    Args:
        description: The description string to clean
        
    Returns:
        Cleaned description string
    """
    # Convert to string and strip whitespace
    description = str(description).strip()
    
    # Remove any duplicate descriptions that might be separated by newlines or semicolons
    if "\n" in description:
        description = description.split("\n")[0].strip()
    if ";" in description:
        description = description.split(";")[0].strip()
    
    return description

def list_venue_images() -> List[Dict]:
    """Get a list of venue images with their metadata."""
    filenames = [
        "eventsbomb_09464_A_very_elegant_and_luxurious.png",
        "amadeowang99_French_modern_wedding.png",
        "amadeowang99_Luxury_wedding_venue.png",
        "amadeowang99_Rustic_wedding_venue.png",
        "amadeowang99_Modern_wedding_venue.png"
    ]
    folder = "wedding venues"
    
    # Create base URL for blob storage
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    
    images = [
        {
            "image": f"{base_url}/{quote(folder)}/{quote(filename)}",
            "title": clean_title(filename),
            "description": "Elegant wedding venue in Austin",
            "location": "Austin, TX",
            "price": "$$",
            "tags": ["Garden", "Outdoor"],
            "share_url": f"{base_url}/share/{quote(filename)}"
        }
        for filename in filenames
    ]
    return images

def list_dress_images() -> List[Dict]:
    """Get a list of dress images with their metadata."""
    filenames = [
        "alexb_79_Classic_Wedding_Dress.png",
        "amadeowang99_Modern_Wedding_Dress.png",
        "amadeowang99_Luxury_Wedding_Dress.png",
        "amadeowang99_Rustic_Wedding_Dress.png",
        "amadeowang99_Bohemian_Wedding_Dress.png"
    ]
    folder = "wedding dresses"
    
    # Create base URL for blob storage
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    
    return [
        {
            "image": f"{base_url}/{quote(folder)}/{quote(filename)}",
            "title": clean_title(filename),
            "description": "Beautiful wedding dress",
            "designer": "Designer Collection",
            "price": "$$$",
            "tags": ["Dress", "Wedding"],
            "share_url": f"{base_url}/share/{quote(filename)}"
        }
        for filename in filenames
    ]

def list_hairstyle_images() -> List[Dict]:
    """Get a list of hairstyle images with their metadata."""
    filenames = [
        "alexb_79_Classic_Wedding_Hairstyle.png",
        "amadeowang99_Modern_Wedding_Hairstyle.png",
        "amadeowang99_Luxury_Wedding_Hairstyle.png",
        "amadeowang99_Rustic_Wedding_Hairstyle.png",
        "amadeowang99_Bohemian_Wedding_Hairstyle.png"
    ]
    folder = "wedding hairstyles"
    
    # Create base URL for blob storage
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    
    return [
        {
            "image": f"{base_url}/{quote(folder)}/{quote(filename)}",
            "title": clean_title(filename),
            "description": "Stunning wedding hairstyle",
            "tags": ["Hairstyle", "Wedding"],
            "share_url": f"{base_url}/share/{quote(filename)}"
        }
        for filename in filenames
    ]

def list_cake_images() -> List[Dict]:
    """Get a list of cake images with their metadata."""
    filenames = [
        "alexb_79_Classic_Wedding_Cake.png",
        "amadeowang99_Modern_Wedding_Cake.png",
        "amadeowang99_Luxury_Wedding_Cake.png",
        "amadeowang99_Rustic_Wedding_Cake.png",
        "amadeowang99_Bohemian_Wedding_Cake.png"
    ]
    folder = "wedding cakes"
    
    # Create base URL for blob storage
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    
    return [
        {
            "image": f"{base_url}/{quote(folder)}/{quote(filename)}",
            "title": clean_title(filename),
            "description": "Delicious wedding cake",
            "price": "$$$",
            "tags": ["Cake", "Wedding"],
            "share_url": f"{base_url}/share/{quote(filename)}"
        }
        for filename in filenames
    ]

def get_images_by_category(category: str, style: Optional[str] = None, location: Optional[str] = None) -> Dict:
    """
    Get wedding images for a specific category with optional style and location filters.
    
    Args:
        category: Type of images (venues, dresses, hairstyles, cakes, etc.)
        style: Optional style descriptor (rustic, modern, bohemian, etc.)
        location: Optional location specification
        
    Returns:
        Dictionary containing image data and carousel information
    """
    try:
        # Map category to the appropriate list function
        category_map = {
            "venues": list_venue_images,
            "dresses": list_dress_images,
            "hairstyles": list_hairstyle_images,
            "cakes": list_cake_images
        }
        
        # Get the appropriate list function
        list_function = category_map.get(category.lower())
        if not list_function:
            return {
                "text": f"I couldn't find any images for the category: {category}",
                "carousel": {
                    "title": f"{category.title()} Collection",
                    "items": []
                }
            }
        
        # Get the images
        items = list_function()
        
        # Filter by style if provided
        if style:
            style_lower = style.lower()
            # Look for style in the title, description, and tags
            items = [
                item for item in items if 
                style_lower in item.get("title", "").lower() or
                style_lower in item.get("description", "").lower() or
                any(style_lower in tag.lower() for tag in item.get("tags", []))
            ]
        
        # Filter by location if provided and if the category is venues
        if location and category.lower() == "venues":
            location_lower = location.lower()
            items = [
                item for item in items if 
                location_lower in item.get("location", "").lower()
            ]
        
        # Format the response
        return {
            "text": f"Here are some {style if style else ''} {category} {f'in {location}' if location else ''}!",
            "carousel": {
                "title": f"{category.title()} Collection",
                "items": items
            }
        }
    except Exception as e:
        print(f"Error in get_images_by_category: {e}")
        return {
            "text": f"I encountered an error while fetching {category} images.",
            "carousel": {
                "title": f"{category.title()} Collection",
                "items": []
            }
        } 