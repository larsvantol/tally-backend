from rest_framework import serializers
from .models import Customer, Transaction, SubTransaction, SubPurchase
from products.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'prefix', 'last_name']

class SubTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTransaction
        fields = ['id', 'description', 'amount']	

class SubPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPurchase
        fields = ['id', 'transaction', 'product', 'quantity', 'price', 'amount']	

class TransactionSerializer(serializers.ModelSerializer):
    subtransactions = SubTransactionSerializer(many=True, read_only=True)
    subpurchases = SubPurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'customer', 'date_created', 'subtransactions', 'subpurchases']