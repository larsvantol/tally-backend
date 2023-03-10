from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Customer, Transaction, SubPurchase
from .serializers import CustomerSerializer, TransactionSerializer, SubPurchaseSerializer

GET_LIST = "list"
GET_RETRIEVE = "retrieve"
POST_CREATE = "create"
DELETE_DESTROY = "destroy"
PUT_UPDATE = "update"
PATCH_PARTIAL_UPDATE = "partial_update"

class SubPurchaseViewSet(viewsets.ModelViewSet):
    queryset = SubPurchase.objects.all()
    serializer_class = SubPurchaseSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing customers.
    """
    
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
        queryset = self.get_queryset().order_by('date_created')
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action == GET_LIST:
            permission_classes = [AllowAny]
        elif self.action == GET_RETRIEVE:
            permission_classes = [AllowAny]
        elif self.action == POST_CREATE:
            permission_classes = [AllowAny]
        elif self.action == PUT_UPDATE:
            permission_classes = [AllowAny]
        elif self.action == PATCH_PARTIAL_UPDATE:
            permission_classes = [AllowAny]
        elif self.action == DELETE_DESTROY:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]