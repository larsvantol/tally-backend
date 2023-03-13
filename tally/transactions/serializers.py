from rest_framework import serializers
from .models import Customer, Transaction, SubTransaction, SubPurchase
from products.serializers import ProductSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'prefix', 'last_name', 'relation_code']
        extra_kwargs = {
            'relation_code': {'write_only': True}
        }

class SubTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTransaction
        fields = ['description', 'amount']	

class SubPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPurchase
        fields = ['product', 'quantity', 'price', 'amount']	
        extra_kwargs = {'price': {'read_only': True}}

class TransactionSerializer(serializers.ModelSerializer):
    subtransactions = SubTransactionSerializer(many=True, read_only=False, required=False)
    subpurchases = SubPurchaseSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'customer', 'date', 'subtransactions', 'subpurchases']

    def create(self, validated_data):
        if not validated_data.get('subtransactions') and not validated_data.get('subpurchases'):
            raise serializers.ValidationError('Transaction must have at least one subtransaction or subpurchase')

        subtransactions_data = validated_data.pop('subtransactions', [])
        subpurchases_data = validated_data.pop('subpurchases', [])

        transaction = Transaction.objects.create(**validated_data)

        for subtransaction_data in subtransactions_data:
            SubTransaction.objects.create(transaction=transaction, **subtransaction_data)

        for subpurchase_data in subpurchases_data:
            SubPurchase.objects.create(transaction=transaction, **subpurchase_data)
        
        return transaction