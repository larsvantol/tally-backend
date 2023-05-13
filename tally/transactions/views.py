from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Customer, Transaction, SubTransaction, SubPurchase
from .serializers import CustomerSerializer, TransactionSerializer

GET_LIST = "list"
GET_RETRIEVE = "retrieve"
GET_TRANSACTION_ROWS = "rows"
GET_CUSTOMER_TRANSACTIONS = "transactions"
POST_CREATE = "create"
DELETE_DESTROY = "destroy"
PUT_UPDATE = "update"
PATCH_PARTIAL_UPDATE = "partial_update"


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing customers.
    """

    @action(detail=True, methods=["get", "post"])
    def transactions(self, request, pk=None):
        """
        Lists transactions for a customer
        """

        # Check if method is GET
        if request.method == "GET":
            queryset = Transaction.objects.filter(customer__id=pk).order_by("date")
            serializer = TransactionSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            if "start_date" not in request.data:
                return Response("Missing start_date", status=400)
            if "end_date" not in request.data:
                return Response("Missing end_date", status=400)

            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")

            queryset = Transaction.objects.filter(
                customer__id=pk, date__range=[start_date, end_date]
            ).order_by("date")
            serializer = TransactionSerializer(queryset, many=True)
            return Response(serializer.data)

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action == GET_LIST:
            permission_classes = [AllowAny]
        elif self.action == GET_RETRIEVE:
            permission_classes = [AllowAny]
        elif self.action == GET_CUSTOMER_TRANSACTIONS:
            permission_classes = [AllowAny]
        elif self.action == POST_CREATE:
            permission_classes = [AllowAny]
        elif self.action == PUT_UPDATE:
            permission_classes = [AllowAny]
        elif self.action == DELETE_DESTROY:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class TransactionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing products.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request):
        """
        Lists products sorted by product group
        """
        queryset = self.get_queryset().order_by("date")
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def list_transactions(self, request):
        """
        Lists transactions for a customer
        """
        list_of_transactions = []

        for transaction in self.get_queryset():
            for sub_transaction in SubTransaction.objects.filter(
                transaction=transaction
            ):
                list_of_transactions.append(
                    {
                        "name": sub_transaction.description,
                        "quantity": 1,
                        "amount": sub_transaction.amount,
                        "date": transaction.date,
                    }
                )
            for sub_purchase in SubPurchase.objects.filter(transaction=transaction):
                list_of_transactions.append(
                    {
                        "name": sub_purchase.product.name,
                        "quantity": sub_purchase.quantity,
                        "amount": sub_purchase.amount(),
                        "date": transaction.date,
                    }
                )

        return Response(list_of_transactions)

    #     [
    #   {name: 'Doritos', quantity: 1, amount: 0.50, date: new Date()},
    #   {name: 'Croky Paprika Chips', quantity: 1, amount: 0.50, date: new Date("2023-03-23")},
    #   {name: 'Doritos', quantity: 1, amount: 0.50, date: new Date("2023-03-20")},
    #   {name: 'Kitkat', quantity: 1, amount: 0.50, date: new Date("2023-03-10")}
    # ];

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action == GET_LIST:
            permission_classes = [AllowAny]
        elif self.action == GET_RETRIEVE:
            permission_classes = [AllowAny]
        elif self.action == GET_TRANSACTION_ROWS:
            permission_classes = [AllowAny]
        elif self.action == POST_CREATE:
            permission_classes = [AllowAny]
        elif self.action == PUT_UPDATE:
            permission_classes = [AllowAny]
        elif self.action == PATCH_PARTIAL_UPDATE:
            permission_classes = [AllowAny]
        elif self.action == DELETE_DESTROY:
            permission_classes = [AllowAny]
        elif self.action == "list_transactions":
            permission_classes = [AllowAny]
        else:
            print(self.action)
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
