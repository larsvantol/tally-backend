from rest_framework import routers

from .views import CustomerViewSet, TransactionViewSet, SubPurchaseViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'customers', CustomerViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'subpurchases', SubPurchaseViewSet)