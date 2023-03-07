from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, ProductGroup
from .serializers import ProductSerializer, ProductGroupSerializer

class ProductGroupViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing product groups.
    """
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
