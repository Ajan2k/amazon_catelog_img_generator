from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TemplateViewSet, ImageAssetViewSet, LogoViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'templates', TemplateViewSet, basename='template')
router.register(r'images', ImageAssetViewSet, basename='image')
router.register(r'logos', LogoViewSet, basename='logo')

urlpatterns = [
    path('', include(router.urls)),
]