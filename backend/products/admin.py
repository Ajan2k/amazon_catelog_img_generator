from django.contrib import admin
from .models import Product, ImageAsset, Template, GenerationJob, Logo


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'created_at']
    search_fields = ['name', 'sku']
    list_filter = ['created_at']


@admin.register(ImageAsset)
class ImageAssetAdmin(admin.ModelAdmin):
    list_display = ['product', 'kind', 'created_at']
    list_filter = ['kind', 'created_at']
    search_fields = ['product__name']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind', 'is_active', 'created_at']
    list_filter = ['kind', 'is_active']
    search_fields = ['name']


@admin.register(GenerationJob)
class GenerationJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'completed_at']


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_default', 'created_at']
    list_filter = ['is_default']