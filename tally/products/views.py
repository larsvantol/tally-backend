from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Product, ProductGroup
from .serializers import ProductGroupSerializer, ProductSerializer


class ProductGroupViewSet(ReadOnlyModelViewSet):
    """
    A read-only ViewSet for viewing product groups.
    """

    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer
    permission_classes = [AllowAny]

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
    A read-only ViewSet for viewing products.
    """

    queryset = Product.objects.all().order_by("product_group__name")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
