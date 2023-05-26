from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Product, ProductGroup
from .serializers import ProductSerializer, ProductGroupSerializer


class ProductGroupViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing product groups.
    """

    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing products.
    """

    queryset = Product.objects.all().order_by("product_group__name")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
