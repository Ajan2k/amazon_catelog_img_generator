from django.conf import settings
import os


def get_media_path(relative_path):
    """Get full path for media file"""
    return os.path.join(settings.MEDIA_ROOT, relative_path)


def get_logo_path():
    """Get path to default logo"""
    from products.models import Logo
    
    logo = Logo.objects.filter(is_default=True).first()
    if logo and logo.image:
        return logo.image.path
    
    # Fallback to a default logo if exists
    default_path = os.path.join(settings.MEDIA_ROOT, 'logos', 'default.png')
    if os.path.exists(default_path):
        return default_path
    
    return None


def replace_template_variables(text, context):
    """Replace template variables like {{product_name}}"""
    for key, value in context.items():
        text = text.replace(f"{{{{{key}}}}}", str(value))
    return text