# backend/generation/templates.py

COLOR_RED = [255, 0, 0, 255]
COLOR_BLACK = [0, 0, 0, 255]
COLOR_GREY = [100, 100, 100, 255]
COLOR_WHITE = [255, 255, 255, 255]

LOGO_DEFAULT = {"position": [1750, 80], "scale": 0.25}

TEMPLATES = {
    "main_hero": {
        "name": "01. Main Hero Image",
        "kind": "main",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 1000, "y": 1000, "scale": 0.85, "rotate": 0},
        "logo": LOGO_DEFAULT,
        "text": [] 
    },

    "lifestyle_compare": {
        "name": "02. Lifestyle Comparison",
        "kind": "lifestyle",
        "canvas_size": [2000, 2000],
        # LINK TO YOUR ASSET HERE:
        "background_asset": "backgrounds/living_room_blurred.jpg", 
        "product_position": {"x": 1400, "y": 1100, "scale": 0.9, "rotate": 0},
        "text": [
            {
                "content": "COMPARE THE KEYS",
                "position": [100, 100],
                "font_size": 110,
                "color": COLOR_RED,
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

    "compatibility": {
        "name": "03. Compatibility Check",
        "kind": "compatibility",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 1000, "y": 1300, "scale": 0.8, "rotate": 0},
        "overlays": [
            # LINK TO AC UNIT ASSET
            {"path": "elements/ac_unit_blowing.png", "position": [500, 400], "scale": 1.0} 
        ],
        "text": [
            {
                "content": "COMPATIBLE WITH",
                "position": [100, 100],
                "font_size": 100,
                "color": COLOR_RED
            },
            {
                "content": "{{product_name}}",
                "position": [1000, 300],
                "font_size": 80,
                "color": COLOR_BLACK,
                "align": "center"
            }
        ],
        "logo": LOGO_DEFAULT
    },

    "battery_info": {
        "name": "04. Battery Info",
        "kind": "feature",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 600, "y": 1100, "scale": 0.85, "rotate": -5},
        "overlays": [
            # LINK TO BATTERIES ASSET
            {"path": "elements/aaa_batteries.png", "position": [1300, 900], "scale": 0.8}
        ],
        "text": [
            {
                "content": "WORKS ON AAA BATTERIES",
                "position": [1400, 1300],
                "font_size": 80,
                "color": COLOR_RED,
                "align": "center"
            }
        ],
        "logo": LOGO_DEFAULT
    },
    
    "pairing": {
        "name": "06. Pairing Instructions",
        "kind": "usage",
        "canvas_size": [2000, 2000],
        "background_color": COLOR_WHITE,
        "product_position": {"x": 600, "y": 1100, "scale": 1.0, "rotate": 0},
        "overlays": [
             # LINK TO VOICE BANNER
            {"path": "elements/voice_control_banner.png", "position": [1200, 1700], "scale": 1.0}
        ],
        "text": [
            {
                "content": "FOR PAIRING",
                "position": [1300, 600],
                "font_size": 110,
                "color": COLOR_BLACK,
            }
        ],
        "logo": LOGO_DEFAULT
    },
}

def get_template_spec(template_name):
    return TEMPLATES.get(template_name, TEMPLATES["main_hero"])

def get_all_templates():
    return TEMPLATES