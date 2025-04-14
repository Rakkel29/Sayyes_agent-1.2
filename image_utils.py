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

def get_images_by_category(category, style=None, location=None):
    """
    Get images for a category with optional filters.
    
    Args:
        category: Type of images (venues, dresses, hairstyles, cakes)
        style: Optional style filter
        location: Optional location filter
        
    Returns:
        Dictionary with image data
    """
    try:
        # Call the appropriate function based on category
        if category.lower() == "venues":
            items = get_venue_images()
        elif category.lower() == "dresses":
            items = get_dress_images()
        elif category.lower() == "hairstyles":
            items = get_hairstyle_images()
        elif category.lower() == "cakes":
            items = get_cake_images()
        else:
            # Default: empty items
            items = []
        
        # Apply style filter if provided
        if style and items:
            items = [item for item in items if style.lower() in item.get("title", "").lower() or 
                    style.lower() in item.get("description", "").lower() or
                    any(style.lower() in tag.lower() for tag in item.get("tags", []))]
        
        # Apply location filter if provided for venues
        if location and category.lower() == "venues" and items:
            items = [item for item in items if location.lower() in item.get("location", "").lower()]
        
        # Return the formatted response
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

def get_venue_images():
    """Get venue images."""
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    folder = "wedding venues"
    
    return [
        {
            "image": f"{base_url}/{quote(folder)}/eventsbomb_09464_A_very_elegant_and_luxurious.png",
            "title": "Elegant Luxurious Venue",
            "description": "A very elegant and luxurious wedding venue",
            "location": "Austin, TX",
            "price": "$$$",
            "tags": ["Elegant", "Luxury", "Indoor"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_French_modern_wedding.png",
            "title": "French Modern Wedding",
            "description": "Beautiful modern venue with French influences",
            "location": "Paris, France",
            "price": "$$$$",
            "tags": ["Modern", "French", "Elegant"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Luxury_wedding_venue.png",
            "title": "Luxury Wedding Venue",
            "description": "Opulent venue with luxurious details",
            "location": "New York, NY",
            "price": "$$$$$",
            "tags": ["Luxury", "Opulent", "Grand"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Rustic_wedding_venue.png",
            "title": "Rustic Wedding Venue",
            "description": "Charming rustic venue with natural elements",
            "location": "Montana",
            "price": "$$",
            "tags": ["Rustic", "Barn", "Natural"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Modern_wedding_venue.png",
            "title": "Modern Wedding Venue",
            "description": "Contemporary venue with sleek design",
            "location": "Los Angeles, CA",
            "price": "$$$",
            "tags": ["Modern", "Contemporary", "Urban"]
        }
    ]

def get_dress_images():
    """Get dress images."""
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    folder = "wedding dresses"
    
    return [
        {
            "image": f"{base_url}/{quote(folder)}/alexb_79_Classic_Wedding_Dress.png",
            "title": "Classic Wedding Dress",
            "description": "Timeless elegant wedding gown",
            "designer": "Classic Bridal",
            "price": "$$$",
            "tags": ["Classic", "Elegant", "Traditional"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Modern_Wedding_Dress.png",
            "title": "Modern Wedding Dress",
            "description": "Contemporary sleek wedding gown",
            "designer": "Modern Bride",
            "price": "$$$",
            "tags": ["Modern", "Sleek", "Minimalist"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Luxury_Wedding_Dress.png",
            "title": "Luxury Wedding Dress",
            "description": "Opulent detailed wedding gown",
            "designer": "Luxury Couture",
            "price": "$$$$",
            "tags": ["Luxury", "Opulent", "Detailed"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Rustic_Wedding_Dress.png",
            "title": "Rustic Wedding Dress",
            "description": "Natural bohemian wedding gown",
            "designer": "Rustic Bride",
            "price": "$$",
            "tags": ["Rustic", "Bohemian", "Natural"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Bohemian_Wedding_Dress.png",
            "title": "Bohemian Wedding Dress",
            "description": "Free-spirited boho wedding gown",
            "designer": "Boho Bridal",
            "price": "$$",
            "tags": ["Bohemian", "Boho", "Flowy"]
        }
    ]

def get_hairstyle_images():
    """Get hairstyle images."""
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    folder = "wedding hairstyles"
    
    return [
        {
            "image": f"{base_url}/{quote(folder)}/alexb_79_Classic_Wedding_Hairstyle.png",
            "title": "Classic Wedding Hairstyle",
            "description": "Timeless elegant updo",
            "tags": ["Classic", "Elegant", "Updo"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Modern_Wedding_Hairstyle.png",
            "title": "Modern Wedding Hairstyle",
            "description": "Contemporary sleek style",
            "tags": ["Modern", "Sleek", "Contemporary"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Luxury_Wedding_Hairstyle.png",
            "title": "Luxury Wedding Hairstyle",
            "description": "Glamorous detailed style",
            "tags": ["Luxury", "Glamorous", "Detailed"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Rustic_Wedding_Hairstyle.png",
            "title": "Rustic Wedding Hairstyle",
            "description": "Natural bohemian style",
            "tags": ["Rustic", "Bohemian", "Natural"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Bohemian_Wedding_Hairstyle.png",
            "title": "Bohemian Wedding Hairstyle",
            "description": "Free-spirited boho style",
            "tags": ["Bohemian", "Boho", "Flowy"]
        }
    ]

def get_cake_images():
    """Get cake images."""
    base_url = f"https://{VERCEL_PROJECT_ID}.public.blob.vercel-storage.com"
    folder = "wedding cakes"
    
    return [
        {
            "image": f"{base_url}/{quote(folder)}/alexb_79_Classic_Wedding_Cake.png",
            "title": "Classic Wedding Cake",
            "description": "Timeless elegant tiered cake",
            "price": "$$$",
            "tags": ["Classic", "Elegant", "Traditional"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Modern_Wedding_Cake.png",
            "title": "Modern Wedding Cake",
            "description": "Contemporary minimalist cake",
            "price": "$$$",
            "tags": ["Modern", "Minimalist", "Geometric"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Luxury_Wedding_Cake.png",
            "title": "Luxury Wedding Cake",
            "description": "Opulent detailed multi-tier cake",
            "price": "$$$$",
            "tags": ["Luxury", "Opulent", "Detailed"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Rustic_Wedding_Cake.png",
            "title": "Rustic Wedding Cake",
            "description": "Natural rustic naked cake",
            "price": "$$",
            "tags": ["Rustic", "Natural", "Naked Cake"]
        },
        {
            "image": f"{base_url}/{quote(folder)}/amadeowang99_Bohemian_Wedding_Cake.png",
            "title": "Bohemian Wedding Cake",
            "description": "Artistic boho-inspired cake",
            "price": "$$",
            "tags": ["Bohemian", "Boho", "Artistic"]
        }
    ] 