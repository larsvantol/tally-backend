import json

from django.contrib.sessions.models import Session
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from .models import Product, ProductGroup
from .serializers import ProductGroupSerializer, ProductSerializer


class ProductGroupViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing product groups.
    """
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer
    permission_classes = [IsAuthenticated]

    # API endpoint that allows products to be listed per group
    @action(detail=True, methods=["get"])
    def products(self, request, pk=None):
        """
        Lists products sorted by product group
        """
        queryset = Product.objects.filter(product_group__id=pk).order_by("name")
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

class ProductViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing products.
    """

    queryset = Product.objects.all().order_by("product_group__name")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
