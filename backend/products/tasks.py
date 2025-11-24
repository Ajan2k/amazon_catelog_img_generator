from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
import os
import tempfile

# Ensure models are imported correctly
from .models import Product, ImageAsset, Template, GenerationJob, GeneratedImage
from generation.engine import ImageGenerator
from generation.utils import get_logo_path, replace_template_variables

@shared_task
def generate_product_images(job_id):
    """
    Main entry point for Celery. 
    This function was likely missing or not visible due to circular imports.
    """
    try:
        job = GenerationJob.objects.get(id=job_id)
        job.status = 'processing'
        job.started_at = timezone.now()
        job.save()

        product = job.product
        # Assuming 'product_image' is the field name for the cutout
        product_cutout = product.product_image.path 
        
        # Initialize Generator
        generator = ImageGenerator()
        
        # Get Templates
        templates = Template.objects.filter(id__in=job.templates_used)
        
        generated_count = 0
        
        for template in templates:
            try:
                # Prepare Context
                logo_path = get_logo_path(product) # Custom util logic
                context = {
                    "product_name": product.name,
                    # Add other context variables here
                }

                # Generate
                temp_path = generate_single_image(
                    generator, 
                    template, 
                    product_cutout, 
                    logo_path, 
                    context
                )

                # Save to DB
                with open(temp_path, 'rb') as f:
                    gen_img = GeneratedImage(
                        product=product,
                        template=template,
                        job=job
                    )
                    filename = f"gen_{product.id}_{template.id}_{timezone.now().timestamp()}.png"
                    gen_img.image.save(filename, ContentFile(f.read()))
                    gen_img.save()
                
                # Cleanup temp file
                os.remove(temp_path)
                generated_count += 1

            except Exception as e:
                print(f"Error generating template {template.id}: {str(e)}")
                # Optionally log specific template error but continue others

        job.status = 'completed'
        job.completed_at = timezone.now()
        job.save()
        return f"Generated {generated_count} images"

    except Exception as e:
        if 'job' in locals():
            job.status = 'failed'
            job.error_message = str(e)
            job.save()
        raise e

def generate_single_image(generator, template, product_cutout, logo_path, context):
    """
    Helper function to generate one image.
    """
    spec = template.spec
    
    # 1. Determine Background Path
    bg_image_path = None
    
    # Priority A: Database Upload
    if template.background_image:
        bg_image_path = template.background_image.path
    # Priority B: Asset Folder (Specified in templates.py)
    elif spec.get('background_asset'):
        bg_image_path = os.path.join(settings.BASE_DIR, 'assets', spec['background_asset'])
    
    # Create Canvas
    bg_color = tuple(spec.get('background_color', [255, 255, 255]))
    canvas = generator.create_canvas(bg_color, bg_image_path)
    
    # 2. Add Overlays
    if spec.get('overlays'):
        for overlay in spec['overlays']:
            ov_path = os.path.join(settings.BASE_DIR, 'assets', overlay['path'])
            canvas = generator.add_overlay(
                canvas, 
                ov_path, 
                tuple(overlay['position']), 
                overlay.get('scale', 1.0)
            )

    # 3. Place Product
    prod_pos = spec.get('product_position', {})
    canvas = generator.place_product(
        canvas,
        product_cutout,
        position=(prod_pos.get('x', 1000), prod_pos.get('y', 1000)),
        scale=prod_pos.get('scale', 1.0),
        rotate=prod_pos.get('rotate', 0)
    )
    
    # 4. Add Text
    for text_spec in spec.get('text', []):
        content = replace_template_variables(text_spec['content'], context)
        canvas = generator.add_text(
            canvas,
            content,
            position=tuple(text_spec['position']),
            font_size=text_spec.get('font_size', 60),
            color=tuple(text_spec.get('color', [0, 0, 0, 255]))
        )
    
    # 5. Add Logo
    if logo_path and spec.get('logo'):
        logo_spec = spec['logo']
        canvas = generator.add_logo(
            canvas,
            logo_path,
            position=tuple(logo_spec['position']),
            scale=logo_spec.get('scale', 0.2)
        )
    
    # Save
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    generator.save_image(canvas, temp_file.name)
    
    return temp_file.name