from rest_framework import routers
from .views import ProductGroupViewSet, ProductViewSet

router = routers.SimpleRouter()
router.register(r'product_groups', ProductGroupViewSet)
router.register(r'products', ProductViewSet)