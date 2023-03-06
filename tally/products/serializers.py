from rest_framework import serializers
from .models import Product, ProductGroup

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    product_group = ProductGroupSerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'image_url', 'product_group']