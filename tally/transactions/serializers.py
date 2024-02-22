from django.contrib.auth.models import User
from django.utils.timezone import now

from rest_framework import serializers
from .models import Customer, Transaction, SubTransaction, SubPurchase


class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "last_login",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_superuser",
            "days_since_joined",
        ]

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "first_name", "prefix", "last_name", "relation_code"]
        extra_kwargs = {"relation_code": {"write_only": True}}


class SubTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTransaction
        fields = ["description", "amount"]


class SubPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPurchase
        fields = ["product", "quantity", "price", "amount"]
        extra_kwargs = {"price": {"read_only": True}}

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be strictly positive")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    subtransactions = SubTransactionSerializer(
        many=True, read_only=False, required=False
    )
    subpurchases = SubPurchaseSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "customer",
            "date",
            "subtransactions",
            "subpurchases",
        ]

    def create(self, validated_data):
        if not validated_data.get("subtransactions") and not validated_data.get(
            "subpurchases"
        ):
            raise serializers.ValidationError(
                "Transaction must have at least one subtransaction or subpurchase"
            )

        subtransactions_data = validated_data.pop("subtransactions", [])
        subpurchases_data = validated_data.pop("subpurchases", [])

        transaction = Transaction.objects.create(**validated_data)

        for subtransaction_data in subtransactions_data:
            SubTransaction.objects.create(
                transaction=transaction, **subtransaction_data
            )

        for subpurchase_data in subpurchases_data:
            SubPurchase.objects.create(transaction=transaction, **subpurchase_data)

        return transaction
