import os
from urllib.parse import quote
import json
import requests

# Get project ID from environment or use default
VERCEL_PROJECT_ID = os.environ.get('VERCEL_PROJECT_ID', 'hebbkx1anhila5yf')

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
            filtered_items = []
            for item in items:
                # Check title, description, and tags
                if (style.lower() in item.get("title", "").lower() or 
                    style.lower() in item.get("description", "").lower() or 
                    any(style.lower() in tag.lower() for tag in item.get("tags", []))):
                    filtered_items.append(item)
            # Only apply filter if we found matches
            if filtered_items:
                items = filtered_items
        
        # Apply location filter if provided for venues
        if location and category.lower() == "venues" and items:
            filtered_items = []
            for item in items:
                if location.lower() in item.get("location", "").lower():
                    filtered_items.append(item)
            # Only apply filter if we found matches
            if filtered_items:
                items = filtered_items
        
        # Verify that all items have valid fields
        for item in items:
            # Ensure all items have a title
            if not item.get("title"):
                item["title"] = "Wedding " + category.title()
            
            # Ensure all items have a description
            if not item.get("description"):
                item["description"] = f"Beautiful {category} for your special day"
                
            # Ensure all items have tags
            if not item.get("tags"):
                item["tags"] = [category.title(), "Wedding"]
            
            # Add share_url if missing
            if not item.get("share_url"):
                item["share_url"] = item.get("image", "")
        
        # Make sure we have at least one item
        if not items:
            items = get_fallback_images(category)
        
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
                "items": get_fallback_images(category)
            }
        }

def get_venue_images():
    """Get venue images from Vercel Blob Storage."""
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
    """Get dress images from Vercel Blob Storage."""
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
    """Get hairstyle images from Vercel Blob Storage."""
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
    """Get cake images from Vercel Blob Storage."""
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

def get_fallback_images(category):
    """Provide fallback images if the primary source fails."""
    if category.lower() == "venues":
        return [
            {
                "image": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800&auto=format&fit=crop",
                "title": "Garden Wedding Venue",
                "description": "Beautiful garden wedding setup with floral arch",
                "location": "Garden Estate",
                "price": "$$$",
                "tags": ["Garden", "Outdoor", "Floral"]
            },
            {
                "image": "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=800&auto=format&fit=crop",
                "title": "Elegant Ballroom",
                "description": "Luxurious ballroom venue with crystal chandeliers",
                "location": "Luxury Hotel",
                "price": "$$$$",
                "tags": ["Ballroom", "Luxury", "Indoor"]
            }
        ]
    elif category.lower() == "dresses":
        return [
            {
                "image": "https://images.unsplash.com/photo-1594612174519-51e4f6d27557?w=800&auto=format&fit=crop",
                "title": "Elegant Wedding Dress",
                "description": "Classic white wedding gown with lace details",
                "designer": "Bridal Collection",
                "price": "$$$",
                "tags": ["Classic", "Lace", "Elegant"]
            },
            {
                "image": "https://images.unsplash.com/photo-1596443686119-d1fd5e1d2ac8?w=800&auto=format&fit=crop",
                "title": "Modern Wedding Dress",
                "description": "Sleek modern wedding dress design",
                "designer": "Modern Bridal",
                "price": "$$$$",
                "tags": ["Modern", "Sleek", "Minimalist"]
            }
        ]
    elif category.lower() == "hairstyles":
        return [
            {
                "image": "https://images.unsplash.com/photo-1579128860537-4efb8efbe6cb?w=800&auto=format&fit=crop",
                "title": "Elegant Updo",
                "description": "Sophisticated updo with floral accents",
                "tags": ["Updo", "Elegant", "Floral"]
            },
            {
                "image": "https://images.unsplash.com/photo-1513112300738-bbb13af7028e?w=800&auto=format&fit=crop",
                "title": "Romantic Waves",
                "description": "Soft flowing waves with side-swept sections",
                "tags": ["Waves", "Romantic", "Flowing"]
            }
        ]
    elif category.lower() == "cakes":
        return [
            {
                "image": "https://images.unsplash.com/photo-1535254973040-607b474cb50d?w=800&auto=format&fit=crop",
                "title": "Elegant Wedding Cake",
                "description": "Multi-tier white wedding cake with floral decorations",
                "price": "$$$",
                "tags": ["White", "Floral", "Multi-tier"]
            },
            {
                "image": "https://images.unsplash.com/photo-1622896784083-cc051313dbab?w=800&auto=format&fit=crop",
                "title": "Modern Wedding Cake",
                "description": "Contemporary wedding cake design with gold accents",
                "price": "$$$$",
                "tags": ["Modern", "Gold", "Contemporary"]
            }
        ]
    else:
        return [
            {
                "image": "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800&auto=format&fit=crop",
                "title": "Wedding Inspiration",
                "description": "Beautiful wedding inspiration",
                "tags": ["Wedding", "Inspiration"]
            }
        ] 