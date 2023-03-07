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

    # Return products sorted by product group
    def get_queryset(self):
        queryset = Product.objects.all().order_by('product_group__name')
        return queryset