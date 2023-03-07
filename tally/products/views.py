from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Product, ProductGroup
from .serializers import ProductSerializer, ProductGroupSerializer

class ProductGroupViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing product groups.
    """
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Returns all products
        """
        queryset = Product.objects.all()
        return queryset

    def list(self, request):
        """
        Lists products sorted by product group
        """
        queryset = self.get_queryset().order_by('product_group__name')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]