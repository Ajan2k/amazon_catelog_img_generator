
from rest_framework import serializers
from .models import Product, ImageAsset, Template, GenerationJob, Logo


class ImageAssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageAsset
        fields = ['id', 'kind', 'image', 'url', 'metadata', 'created_at']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ImageAssetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'description', 'images', 'created_at', 'updated_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    original_image = serializers.ImageField(write_only=True)
    
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'original_image']
    
    def create(self, validated_data):
        original_image = validated_data.pop('original_image')
        product = Product.objects.create(**validated_data)
        ImageAsset.objects.create(
            product=product,
            kind='original',
            image=original_image
        )
        return product


class TemplateSerializer(serializers.ModelSerializer):
    background_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Template
        fields = ['id', 'name', 'description', 'kind', 'spec', 'background_image', 
                  'background_url', 'preview_image', 'is_active', 'created_at']
    
    def get_background_url(self, obj):
        request = self.context.get('request')
        if obj.background_image and request:
            return request.build_absolute_uri(obj.background_image.url)
        return None


class GenerationJobSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = GenerationJob
        fields = ['id', 'product', 'product_name', 'status', 'templates_used', 
                  'result', 'error_message', 'created_at', 'completed_at']
        read_only_fields = ['status', 'result', 'error_message', 'completed_at']


class LogoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Logo
        fields = ['id', 'name', 'image', 'url', 'is_default', 'created_at']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None