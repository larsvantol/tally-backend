import json

from django.contrib.sessions.models import Session
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Product, ProductGroup
from .serializers import ProductGroupSerializer, ProductSerializer


class ProductGroupViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing product groups.
    """

    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, format=None):
        print(f"Cookie:\t{request.COOKIES}")
        print(f"Headers:\t{json.dumps(dict(request.headers), indent=2)}")
        print(f"Session:\t{request.session}")
        print(f"User:\t{request.user}")
        print(f"Auth:\t{request.auth}")

        sessions = Session.objects.iterator()  # also works with Session.objects.get_queryset()
        for session in sessions:  # iterate over sessions
            data = session.get_decoded()  # decode the session data
            data["session_key"] = (
                session.session_key
            )  # normally the data doesn't include the session key, so add it
            print(f"Session:\t{json.dumps(data, indent=2)}")
        return super().list(request, format)


class ProductViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing products.
    """

    queryset = Product.objects.all().order_by("product_group__name")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
