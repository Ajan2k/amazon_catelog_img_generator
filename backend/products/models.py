from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.sku})"


class ImageAsset(models.Model):
    IMAGE_KINDS = [
        ('original', 'Original Upload'),
        ('main', 'Main Product Image'),
        ('lifestyle', 'Lifestyle Image'),
        ('feature', 'Feature Callouts'),
        ('usage', 'Usage Image'),
        ('dimensions', 'Size/Dimensions'),
        ('packaging', 'Packaging/Back'),
        ('comparison', 'Comparison/Highlight'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    kind = models.CharField(max_length=50, choices=IMAGE_KINDS)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['kind']
    
    def __str__(self):
        return f"{self.product.name} - {self.kind}"


class Template(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    kind = models.CharField(max_length=50)  # lifestyle, feature, etc.
    spec = models.JSONField()
    background_image = models.ImageField(upload_to='templates/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preview_image = models.ImageField(upload_to='template_previews/', null=True, blank=True)
    
    def __str__(self):
        return self.name


class GenerationJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    templates_used = models.JSONField(default=list)
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Job {self.id} - {self.product.name} - {self.status}"


class Logo(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='logos/')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Logo.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)