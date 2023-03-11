from rest_framework import routers

from .views import CustomerViewSet, TransactionViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'transactions', TransactionViewSet)