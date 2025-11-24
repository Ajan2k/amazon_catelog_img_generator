from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True)
    # ADDED: This field was missing
    description = models.TextField(blank=True, null=True) 
    product_image = models.ImageField(upload_to='products/originals/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=50, default='social')
    spec = models.JSONField(default=dict) 
    background_image = models.ImageField(upload_to='templates/backgrounds/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ImageAsset(models.Model):
    product = models.ForeignKey(Product, related_name='assets', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='assets/')
    kind = models.CharField(max_length=50)
    # Added created_at to fix Admin error
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.kind})"

class Logo(models.Model):
    name = models.CharField(max_length=255, default="Default Logo")
    image = models.ImageField(upload_to='logos/')
    is_default = models.BooleanField(default=False)
    # Added created_at to fix Admin error
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Logo.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class GenerationJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    product = models.ForeignKey(Product, related_name='jobs', on_delete=models.CASCADE)
    templates_used = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id} - {self.product.name} ({self.status})"

class GeneratedImage(models.Model):
    product = models.ForeignKey(Product, related_name='generated_images', on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(GenerationJob, related_name='generated_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='generated/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gen Image for {self.product.name}"