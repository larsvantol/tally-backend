from rest_framework import routers

from .views import ProductGroupViewSet, ProductViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'product_groups', ProductGroupViewSet)
router.register(r'products', ProductViewSet)