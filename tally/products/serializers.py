from rest_framework import serializers
from .models import Product, ProductGroup

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    product_group_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """

        # Check if stock is in validated_data
        if 'stock' not in validated_data:
            validated_data['stock'] = 0
        # Check if image_url is in validated_data
        if 'image_url' not in validated_data:
            validated_data['image_url'] = ''

        # Check if a product group with primary key product_group_id exists
        product_group = ProductGroup.objects.filter(pk=validated_data['product_group_id'])
        if product_group.exists():
            return Product.objects.create(name=validated_data['name'], 
                                        price=validated_data['price'], 
                                        stock=validated_data['stock'], 
                                        image_url=validated_data['image_url'], 
                                        product_group=product_group.get()
                                        )
        else:
            raise serializers.ValidationError(f"product_group_id: Product group with id {validated_data['product_group_id']} does not exist")

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'image_url', 'product_group', 'product_group_id']
        depth = 1