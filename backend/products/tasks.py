from celery import shared_task
from django.core.files.base import ContentFile
from django.utils import timezone
import os
import tempfile

from .models import Product, ImageAsset, Template, GenerationJob, Logo
from generation.engine import ImageGenerator
from generation.utils import get_logo_path, replace_template_variables


@shared_task
def generate_product_images(job_id):
    """Generate all 7 product images based on templates"""
    try:
        job = GenerationJob.objects.get(id=job_id)
        job.status = 'processing'
        job.save()
        
        product = job.product
        template_ids = job.templates_used
        
        # Get original product image
        original_image = product.images.filter(kind='original').first()
        if not original_image:
            raise Exception("No original image found for product")
        
        # Initialize generator
        generator = ImageGenerator()
        
        # Remove background from original image
        product_cutout = generator.remove_background(original_image.image.path)
        
        # Get logo path
        logo_path = get_logo_path()
        
        # Template variable context
        context = {
            'product_name': product.name,
            'sku': product.sku,
            'description': product.description
        }
        
        generated_images = []
        
        # Process each template
        templates = Template.objects.filter(id__in=template_ids, is_active=True)
        
        for template in templates:
            try:
                # Generate image for this template
                output_path = generate_single_image(
                    generator, 
                    template, 
                    product_cutout, 
                    logo_path, 
                    context
                )
                
                # Save to database
                with open(output_path, 'rb') as f:
                    image_asset = ImageAsset.objects.create(
                        product=product,
                        kind=template.kind,
                        metadata={
                            'template_id': template.id,
                            'template_name': template.name
                        }
                    )
                    image_asset.image.save(
                        f"{product.sku}_{template.kind}.png",
                        ContentFile(f.read()),
                        save=True
                    )
                
                generated_images.append({
                    'kind': template.kind,
                    'template': template.name,
                    'url': image_asset.image.url
                })
                
                # Clean up temp file
                os.unlink(output_path)
                
            except Exception as e:
                print(f"Error generating image for template {template.name}: {str(e)}")
                continue
        
        # Update job status
        job.status = 'completed'
        job.result = {
            'generated_count': len(generated_images),
            'images': generated_images
        }
        job.completed_at = timezone.now()
        job.save()
        
        return {
            'success': True,
            'job_id': job_id,
            'generated': len(generated_images)
        }
        
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        return {
            'success': False,
            'job_id': job_id,
            'error': str(e)
        }


def generate_single_image(generator, template, product_cutout, logo_path, context):
    """Generate a single image based on template spec"""
    spec = template.spec
    
    # Create canvas
    bg_color = tuple(spec.get('background_color', [255, 255, 255]))
    bg_image = template.background_image.path if template.background_image else None
    canvas = generator.create_canvas(bg_color, bg_image)
    
    # Place product
    prod_pos = spec.get('product_position', {})
    canvas = generator.place_product(
        canvas,
        product_cutout,
        position=(prod_pos.get('x', 1000), prod_pos.get('y', 1000)),
        scale=prod_pos.get('scale', 1.0),
        rotate=prod_pos.get('rotate', 0)
    )
    
    # Add text elements
    for text_spec in spec.get('text', []):
        content = replace_template_variables(text_spec['content'], context)
        canvas = generator.add_text(
            canvas,
            content,
            position=tuple(text_spec['position']),
            font_size=text_spec.get('font_size', 60),
            color=tuple(text_spec.get('color', [0, 0, 0, 255])),
            max_width=text_spec.get('max_width')
        )
    
    # Add arrows (for feature callouts)
    for arrow_spec in spec.get('arrows', []):
        canvas = generator.add_arrow(
            canvas,
            start=tuple(arrow_spec['start']),
            end=tuple(arrow_spec['end']),
            color=tuple(arrow_spec.get('color', [255, 0, 0, 255]))
        )
    
    # Add dimension lines
    if spec.get('show_dimensions'):
        canvas = generator.add_dimension_lines(
            canvas,
            bbox=spec.get('dimension_bbox', [400, 400, 1600, 1400]),
            dimensions_text=spec.get('dimensions_text', {})
        )
    
    # Add logo
    if logo_path and spec.get('logo'):
        logo_spec = spec['logo']
        canvas = generator.add_logo(
            canvas,
            logo_path,
            position=tuple(logo_spec['position']),
            scale=logo_spec.get('scale', 0.2)
        )
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    generator.save_image(canvas, temp_file.name)
    
    return temp_file.name