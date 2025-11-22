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
    
    def remove_background(self, image_path):
        """Remove background from product image"""
        with open(image_path, 'rb') as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)
            
        image = Image.open(BytesIO(output_data))
        return image
    
    def create_canvas(self, background_color=(255, 255, 255), background_image=None):
        """Create base canvas with optional background image"""
        if background_image:
            bg = Image.open(background_image)
            bg = bg.resize(self.canvas_size, Image.Resampling.LANCZOS)
            canvas = bg.convert('RGBA')
        else:
            canvas = Image.new('RGBA', self.canvas_size, background_color + (255,))
        
        return canvas
    
    def place_product(self, canvas, product_image, position, scale=1.0, rotate=0):
        """Place product on canvas with transformations"""
        # Ensure product image has transparency
        if product_image.mode != 'RGBA':
            product_image = product_image.convert('RGBA')
        
        # Scale
        if scale != 1.0:
            new_size = tuple(int(dim * scale) for dim in product_image.size)
            product_image = product_image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Rotate
        if rotate != 0:
            product_image = product_image.rotate(rotate, expand=True, resample=Image.Resampling.BICUBIC)
        
        # Calculate position
        x, y = position
        x = int(x - product_image.width / 2)  # Center on position
        y = int(y - product_image.height / 2)
        
        # Paste with alpha channel
        canvas.paste(product_image, (x, y), product_image)
        
        return canvas
    
    def add_text(self, canvas, text, position, font_path=None, font_size=None, 
                 color=(0, 0, 0, 255), align='left', max_width=None):
        """Add text to canvas"""
        draw = ImageDraw.Draw(canvas)
        
        # Load font
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size or self.default_font_size)
        else:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", #this file path only exist in linux server when run this on windows program would crash that why we used try here
                                         font_size or self.default_font_size)
            except:
                font = ImageFont.load_default()
        
        # Word wrap if max_width specified
        if max_width:
            text = self._wrap_text(text, font, max_width)
        
        # Draw text
        draw.text(position, text, fill=color, font=font, align=align)
        
        return canvas
    
    def add_logo(self, canvas, logo_path, position, scale=0.2):
        """Add logo to canvas"""
        logo = Image.open(logo_path)
        
        # Convert to RGBA if needed
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Scale logo
        new_size = tuple(int(dim * scale) for dim in logo.size)
        logo = logo.resize(new_size, Image.Resampling.LANCZOS)
        
        # Paste logo
        canvas.paste(logo, position, logo)
        
        return canvas
    
    def add_arrow(self, canvas, start, end, color=(255, 0, 0, 255), width=5):
        """Add arrow pointing to feature"""
        draw = ImageDraw.Draw(canvas)
        
        # Draw line
        draw.line([start, end], fill=color, width=width)
        
        # Draw arrowhead
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        arrow_length = 30
        arrow_angle = np.pi / 6
        
        point1 = (
            int(end[0] - arrow_length * np.cos(angle - arrow_angle)),
            int(end[1] - arrow_length * np.sin(angle - arrow_angle))
        )
        point2 = (
            int(end[0] - arrow_length * np.cos(angle + arrow_angle)),
            int(end[1] - arrow_length * np.sin(angle + arrow_angle))
        )
        
        draw.polygon([end, point1, point2], fill=color)
        
        return canvas
    
    def add_dimension_lines(self, canvas, bbox, dimensions_text):
        """Add dimension lines with measurements"""
        draw = ImageDraw.Draw(canvas)
        x1, y1, x2, y2 = bbox
        
        # Horizontal line (width)
        line_offset = 50
        draw.line([(x1, y2 + line_offset), (x2, y2 + line_offset)], 
                 fill=(0, 0, 0, 255), width=3)
        draw.line([(x1, y2 + line_offset - 10), (x1, y2 + line_offset + 10)], 
                 fill=(0, 0, 0, 255), width=3)
        draw.line([(x2, y2 + line_offset - 10), (x2, y2 + line_offset + 10)], 
                 fill=(0, 0, 0, 255), width=3)
        
        # Add width text
        width_text = dimensions_text.get('width', 'Width')
        text_pos = ((x1 + x2) // 2 - 50, y2 + line_offset + 20)
        self.add_text(canvas, width_text, text_pos, font_size=40)
        
        # Vertical line (height)
        draw.line([(x2 + line_offset, y1), (x2 + line_offset, y2)], 
                 fill=(0, 0, 0, 255), width=3)
        draw.line([(x2 + line_offset - 10, y1), (x2 + line_offset + 10, y1)], 
                 fill=(0, 0, 0, 255), width=3)
        draw.line([(x2 + line_offset - 10, y2), (x2 + line_offset + 10, y2)], 
                 fill=(0, 0, 0, 255), width=3)
        
        # Add height text
        height_text = dimensions_text.get('height', 'Height')
        text_pos = (x2 + line_offset + 20, (y1 + y2) // 2 - 20)
        self.add_text(canvas, height_text, text_pos, font_size=40)
        
        return canvas
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            print("bbox :",bbox)
            width = bbox[2] - bbox[0]
            print("width :",width)
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def save_image(self, canvas, output_path, format='PNG'):
        """Save canvas to file"""
        # Convert RGBA to RGB if saving as JPEG
        if format.upper() in ['JPEG', 'JPG']:
            canvas = canvas.convert('RGB')
        
        canvas.save(output_path, format=format, quality=95)
        return output_path
    
if __name__ == "__main__":
    test ="Logic: This is the crucial part. It asks the font file: \"If I were to write 'The quick brown' in size 40 Arial, exactly how many pixels wide would it be?\"bbox: Returns (left, top, right, bottom).width: The Right edge minus the Left edge equals the total width."
    obj = ImageGenerator()
    print(obj._wrap_text(text=test, max_width=50,font=ImageFont.load_default()))
    
    