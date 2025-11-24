from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np
from io import BytesIO
from rembg import remove
import os

class ImageGenerator:
    def __init__(self, canvas_size=(2000, 2000)):
        self.canvas_size = canvas_size
        self.default_font_size = 60
    
    def remove_background(self, image_file_obj):
        image_file_obj.seek(0)
        input_data = image_file_obj.read()
        output_data = remove(input_data)
        image = Image.open(BytesIO(output_data))
        return image
    
    def create_canvas(self, background_color=(255, 255, 255), background_image=None):
        if background_image and os.path.exists(background_image):
            bg = Image.open(background_image)
            bg = bg.resize(self.canvas_size, Image.Resampling.LANCZOS)
            canvas = bg.convert('RGBA')
        else:
            canvas = Image.new('RGBA', self.canvas_size, background_color + (255,))
        return canvas
    
    def place_product(self, canvas, product_image, position, scale=1.0, rotate=0):
        if product_image.mode != 'RGBA':
            product_image = product_image.convert('RGBA')
        
        if scale != 1.0:
            new_size = tuple(int(dim * scale) for dim in product_image.size)
            product_image = product_image.resize(new_size, Image.Resampling.LANCZOS)
        
        if rotate != 0:
            product_image = product_image.rotate(rotate, expand=True, resample=Image.Resampling.BICUBIC)
        
        x, y = position
        x = int(x - product_image.width / 2)
        y = int(y - product_image.height / 2)
        
        canvas.paste(product_image, (x, y), product_image)
        return canvas

    def add_overlay(self, canvas, image_path, position, scale=1.0):
        """Add an overlay image (like batteries or banners)"""
        if not os.path.exists(image_path):
            print(f"Warning: Overlay not found at {image_path}")
            return canvas
            
        overlay = Image.open(image_path)
        if overlay.mode != 'RGBA':
            overlay = overlay.convert('RGBA')
            
        if scale != 1.0:
            new_size = tuple(int(dim * scale) for dim in overlay.size)
            overlay = overlay.resize(new_size, Image.Resampling.LANCZOS)
            
        # Position is center-based? Let's make it top-left based for overlays to be easier
        # Or keep consistent: Position is the TOP-LEFT corner of the overlay
        canvas.paste(overlay, position, overlay)
        return canvas
    
    def add_text(self, canvas, text, position, font_path=None, font_size=None, 
                 color=(0, 0, 0, 255), align='left', max_width=None):
        draw = ImageDraw.Draw(canvas)
        
        # Try loading a better font, fallback to default
        font = ImageFont.load_default()
        # You can add a font file to assets/fonts/ and load it here for better look
        
        if max_width:
            text = self._wrap_text(text, font, max_width)
        
        draw.text(position, text, fill=color, font=font, align=align)
        return canvas
    
    def add_logo(self, canvas, logo_path, position, scale=0.2):
        return self.add_overlay(canvas, logo_path, position, scale)
    
    def add_arrow(self, canvas, start, end, color=(255, 0, 0, 255), width=5):
        draw = ImageDraw.Draw(canvas)
        draw.line([start, end], fill=color, width=width)
        return canvas
    
    def add_dimension_lines(self, canvas, bbox, dimensions_text):
        draw = ImageDraw.Draw(canvas)
        x1, y1, x2, y2 = bbox
        
        # Draw lines logic (kept simple for brevity)
        draw.rectangle(bbox, outline=(0,0,0,255), width=3)
        return canvas
    
    def _wrap_text(self, text, font, max_width):
        return text # Simplified for now
    
    def save_image(self, canvas, output_path, format='PNG'):
        canvas.save(output_path, format=format, quality=95)
        return output_path