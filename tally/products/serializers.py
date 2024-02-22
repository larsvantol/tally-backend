from rest_framework import serializers
from .models import Product, ProductGroup


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "image_url", "product_group"]
        depth = 1


class ProductGroupSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductGroup
        fields = ["id", "name", "products"]
