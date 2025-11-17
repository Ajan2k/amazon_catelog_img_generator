from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from .models import Product, ImageAsset, Template, GenerationJob, Logo
from .serializers import (
    ProductSerializer, ProductCreateSerializer, ImageAssetSerializer,
    TemplateSerializer, GenerationJobSerializer, LogoSerializer
)
from .tasks import generate_product_images


@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return ProductSerializer
    
    @action(detail=True, methods=['post'], parser_classes=[JSONParser])
    def generate_images(self, request, pk=None):
        """Trigger image generation for a product"""
        product = self.get_object()
        template_ids = request.data.get('template_ids', [])
        
        # If no templates specified, use all active templates
        if not template_ids:
            templates = Template.objects.filter(is_active=True)
            template_ids = list(templates.values_list('id', flat=True))
        
        # Create generation job
        job = GenerationJob.objects.create(
            product=product,
            templates_used=template_ids,
            status='pending'
        )
        
        # Trigger async task
        generate_product_images.delay(job.id)
        
        return Response({
            'job_id': job.id,
            'status': 'pending',
            'message': 'Image generation started'
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=True, methods=['get'])
    def job_status(self, request, pk=None):
        """Check status of image generation"""
        product = self.get_object()
        job_id = request.query_params.get('job_id')
        
        if job_id:
            job = get_object_or_404(GenerationJob, id=job_id, product=product)
        else:
            job = product.jobs.first()
        
        if not job:
            return Response({'error': 'No generation jobs found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        serializer = GenerationJobSerializer(job)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.filter(is_active=True)
    serializer_class = TemplateSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    @action(detail=False, methods=['get'])
    def by_kind(self, request):
        """Get templates grouped by kind"""
        kind = request.query_params.get('kind')
        if kind:
            templates = self.queryset.filter(kind=kind)
        else:
            templates = self.queryset.all()
        
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class ImageAssetViewSet(viewsets.ModelViewSet):
    queryset = ImageAsset.objects.all()
    serializer_class = ImageAssetSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        kind = self.request.query_params.get('kind')
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if kind:
            queryset = queryset.filter(kind=kind)
        
        return queryset


@method_decorator(csrf_exempt, name='dispatch')
class LogoViewSet(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """Get the default logo"""
        logo = Logo.objects.filter(is_default=True).first()
        if logo:
            serializer = self.get_serializer(logo)
            return Response(serializer.data)
        return Response({'error': 'No default logo set'}, 
                       status=status.HTTP_404_NOT_FOUND)