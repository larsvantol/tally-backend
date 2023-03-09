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
        
    def update(self, instance, validated_data):
        """
        Update and return an existing `Product` instance, given the validated data.
        """

        # Check if stock is in validated_data, if not set stock to current stock
        if 'stock' not in validated_data:
            validated_data['stock'] = instance.stock
        # Check if image_url is in validated_data, if not set image_url to current image_url
        if 'image_url' not in validated_data:
            validated_data['image_url'] = instance.image_url

        # Check if a product group with primary key product_group_id exists
        product_group = ProductGroup.objects.filter(pk=validated_data['product_group_id'])
        if product_group.exists():
            instance.name = validated_data.get('name', instance.name)
            instance.price = validated_data.get('price', instance.price)
            instance.stock = validated_data.get('stock', instance.stock)
            instance.image_url = validated_data.get('image_url', instance.image_url)
            instance.product_group = product_group.get()
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(f"product_group_id: Product group with id {validated_data['product_group_id']} does not exist")

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'image_url', 'product_group', 'product_group_id']
        extra_kwargs = {'stock': {'required': False}}
        depth = 1