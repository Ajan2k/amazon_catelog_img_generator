# Default template specifications

TEMPLATES = {
    "main_product": {
        "name": "Main Product Image",
        "kind": "main",
        "canvas_size": [2000, 2000],
        "background_color": [255, 255, 255],
        "product_position": {"x": 1000, "y": 1000, "scale": 0.8, "rotate": 0},
        "logo": {"position": [1700, 100], "scale": 0.15}
    },
    
    "lifestyle_livingroom": {
        "name": "Lifestyle - Living Room",
        "kind": "lifestyle",
        "canvas_size": [2000, 2000],
        "background_color": [240, 235, 230],
        "product_position": {"x": 1200, "y": 1100, "scale": 0.6, "rotate": -5},
        "text": [
            {
                "content": "{{product_name}}",
                "position": [100, 150],
                "font_size": 80,
                "color": [50, 50, 50, 255],
                "max_width": 800
            },
            {
                "content": "Perfect for your home",
                "position": [100, 280],
                "font_size": 50,
                "color": [100, 100, 100, 255]
            }
        ],
        "logo": {"position": [1700, 100], "scale": 0.15}
    },
    
    "feature_callouts": {
        "name": "Feature Callouts",
        "kind": "feature",
        "canvas_size": [2000, 2000],
        "background_color": [255, 255, 255],
        "product_position": {"x": 700, "y": 1000, "scale": 0.7, "rotate": 0},
        "arrows": [
            {
                "start": [1100, 800],
                "end": [950, 850],
                "color": [255, 87, 51, 255]
            },
            {
                "start": [1100, 1100],
                "end": [950, 1050],
                "color": [255, 87, 51, 255]
            }
        ],
        "text": [
            {
                "content": "Premium Quality",
                "position": [1120, 770],
                "font_size": 50,
                "color": [255, 87, 51, 255]
            },
            {
                "content": "Durable Design",
                "position": [1120, 1070],
                "font_size": 50,
                "color": [255, 87, 51, 255]
            }
        ],
        "logo": {"position": [1700, 100], "scale": 0.15}
    },
    
    "usage_hand": {
        "name": "Usage - In Hand",
        "kind": "usage",
        "canvas_size": [2000, 2000],
        "background_color": [245, 245, 250],
        "product_position": {"x": 1000, "y": 1000, "scale": 0.65, "rotate": 15},
        "text": [
            {
                "content": "Easy to Use",
                "position": [100, 100],
                "font_size": 90,
                "color": [30, 30, 30, 255]
            }
        ],
        "logo": {"position": [1700, 100], "scale": 0.15}
    },
    
    "dimensions": {
        "name": "Size & Dimensions",
        "kind": "dimensions",
        "canvas_size": [2000, 2000],
        "background_color": [255, 255, 255],
        "product_position": {"x": 1000, "y": 900, "scale": 0.7, "rotate": 0},
        "show_dimensions": True,
        "dimension_bbox": [400, 400, 1600, 1400],
        "dimensions_text": {
            "width": "12 inches",
            "height": "8 inches"
        },
        "logo": {"position": [1700, 100], "scale": 0.15}
    },
    
    "comparison": {
        "name": "Key Features Comparison",
        "kind": "comparison",
        "canvas_size": [2000, 2000],
        "background_color": [250, 250, 250],
        "product_position": {"x": 600, "y": 700, "scale": 0.5, "rotate": 0},
        "text": [
            {
                "content": "{{product_name}}",
                "position": [100, 80],
                "font_size": 70,
                "color": [0, 0, 0, 255],
                "max_width": 900
            },
            {
                "content": "✓ High Quality Materials",
                "position": [1100, 400],
                "font_size": 50,
                "color": [34, 139, 34, 255]
            },
            {
                "content": "✓ Long-lasting Durability",
                "position": [1100, 550],
                "font_size": 50,
                "color": [34, 139, 34, 255]
            },
            {
                "content": "✓ Easy to Clean",
                "position": [1100, 700],
                "font_size": 50,
                "color": [34, 139, 34, 255]
            },
            {
                "content": "✓ 1 Year Warranty",
                "position": [1100, 850],
                "font_size": 50,
                "color": [34, 139, 34, 255]
            }
        ],
        "logo": {"position": [100, 1800], "scale": 0.2}
    }
}


def get_template_spec(template_name):
    """Get template specification by name"""
    return TEMPLATES.get(template_name, TEMPLATES["main_product"])


def get_all_templates():
    """Get all available templates"""
    return TEMPLATES