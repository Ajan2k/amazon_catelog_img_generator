# backend/generation/templates.py

# Standard 7Seven Colors
COLOR_RED = [255, 0, 0, 255]
COLOR_BLACK = [0, 0, 0, 255]
COLOR_GREY = [100, 100, 100, 255]
COLOR_WHITE = [255, 255, 255, 255]

# Standard Logo Position (Top Right)
LOGO_DEFAULT = {"position": [1750, 100], "scale": 0.25}

TEMPLATES = {
    # 1. Main Listing Image (Clean White)
    "main_hero": {
        "name": "01. Main Hero Image",
        "kind": "main",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 1000, "y": 1000, "scale": 0.85, "rotate": 0},
        "logo": LOGO_DEFAULT,
        "text": [] 
    },

    # 2. Lifestyle Comparison (Living Room)
    # Note: Requires 'living_room_blurred.jpg' uploaded as background in Admin
    "lifestyle_compare": {
        "name": "02. Lifestyle Comparison",
        "kind": "lifestyle",
        "canvas_size": [2000, 2000],
        "background_color": [240, 240, 240], # Fallback if no image
        "product_position": {"x": 1400, "y": 1100, "scale": 0.9, "rotate": 0},
        "text": [
            {
                "content": "COMPARE THE KEYS",
                "position": [100, 100],
                "font_size": 110,
                "color": COLOR_RED,
                "max_width": 1800
            },
            {
                "content": "Match Your Existing Remote Control\nWith 7Seven Remote Before Ordering",
                "position": [1000, 1850],
                "font_size": 50,
                "color": COLOR_BLACK,
                "align": "center"
            }
        ],
        "logo": LOGO_DEFAULT
    },

    # 3. Compatibility (AC/TV)
    "compatibility": {
        "name": "03. Compatibility Check",
        "kind": "compatibility",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 1000, "y": 1300, "scale": 0.8, "rotate": 0},
        "text": [
            {
                "content": "COMPATIBLE WITH",
                "position": [100, 100],
                "font_size": 100,
                "color": COLOR_RED
            },
            {
                "content": "{{product_name}}", # Dynamic Product Name
                "position": [1000, 300],
                "font_size": 80,
                "color": COLOR_BLACK,
                "align": "center",
                "max_width": 1800
            }
        ],
        "logo": LOGO_DEFAULT
    },

    # 4. Battery Information
    "battery_info": {
        "name": "04. Battery Info",
        "kind": "feature",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 600, "y": 1100, "scale": 0.85, "rotate": -5},
        "text": [
            {
                "content": "WORKS ON",
                "position": [1400, 1200],
                "font_size": 80,
                "color": COLOR_RED,
                "align": "center"
            },
            {
                "content": "AAA BATTERIES",
                "position": [1400, 1300],
                "font_size": 100,
                "color": COLOR_BLACK,
                "align": "center"
            },
            {
                "content": "Using New Batteries is Recommended",
                "position": [1400, 1500],
                "font_size": 40,
                "color": COLOR_GREY,
                "align": "center",
                "max_width": 800
            }
        ],
        "logo": LOGO_DEFAULT
    },

    # 5. Dimensions / Size
    "dimensions": {
        "name": "05. Dimensions",
        "kind": "dimensions",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 1100, "y": 1000, "scale": 0.9, "rotate": 0},
        "show_dimensions": True,
        "dimension_bbox": [600, 200, 1600, 1800], # Box to draw lines around
        "dimensions_text": {
            "width": "Width",
            "height": "Height"
        },
        "logo": LOGO_DEFAULT
    },

    # 6. Pairing Instructions (Voice Remote)
    "pairing": {
        "name": "06. Pairing Instructions",
        "kind": "usage",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 600, "y": 1100, "scale": 1.0, "rotate": 0},
        "text": [
            {
                "content": "FOR PAIRING",
                "position": [1300, 600],
                "font_size": 110,
                "color": [60, 60, 60, 255], # Dark Grey
                "align": "left"
            },
            {
                "content": "Press and Hold designated\nbuttons until the light\nstarts pulsing to pair.",
                "position": [1300, 850],
                "font_size": 55,
                "color": COLOR_GREY,
                "align": "left",
                "max_width": 800
            }
        ],
        "logo": LOGO_DEFAULT
    },
    
    # 7. Side-by-Side Comparison (Check/Cross)
    "comparison_check": {
        "name": "07. Check/Cross Comparison",
        "kind": "comparison",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 600, "y": 1100, "scale": 0.8, "rotate": 0},
        "text": [
            {
                "content": "COMPATIBLE WITH",
                "position": [100, 100],
                "font_size": 100,
                "color": COLOR_RED
            },
            {
                "content": "YOUR OLD REMOTE",
                "position": [1400, 1700],
                "font_size": 60,
                "color": COLOR_GREY,
                "align": "center"
            }
        ],
        # Note: This template ideally needs a secondary image upload, 
        # which the current engine doesn't support yet. 
        # It will place the MAIN product on the left.
        "logo": LOGO_DEFAULT
    }
}


def get_template_spec(template_name):
    """Get template specification by name"""
    return TEMPLATES.get(template_name, TEMPLATES["main_hero"])


def get_all_templates():
    """Get all available templates"""
    return TEMPLATES