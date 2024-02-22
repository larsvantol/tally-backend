from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SubPurchase, SubTransaction, Transaction
from .serializers import CustomerSerializer, TransactionSerializer


class TransactionsView(ListCreateAPIView):
    """
    View to list and create transactions
    A customer can only see their own transactions and create new ones for themselves.
    """

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

    def get_queryset(self):
        customer = self.request.user.customer
        return Transaction.objects.filter(customer=customer).order_by("date")

    def filter_queryset_by_month_if_exists(self, queryset, request):
        if "month" in request.query_params and "year" in request.query_params:
            month = int(request.query_params.get("month"))
            year = int(request.query_params.get("year"))
            return queryset.filter(date__month=month, date__year=year)
        else:
            return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset_by_month_if_exists(self.get_queryset(), request)

        if "flat" in request.query_params and (
            request.query_params.get("flat").lower() == "true"
            or request.query_params.get("flat") == "1"
        ):
            return self.flat_list(queryset)
        else:
            return Response(self.serializer_class(queryset, many=True).data)

    def flat_list(self, transactions):
        list_of_transactions = []

        for transaction in transactions:
            for sub_transaction in SubTransaction.objects.filter(transaction=transaction):
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


class CustomerView(RetrieveAPIView):
    """
    A view to retrieve the information of the customer and the user associated with it.
    """

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.customer
