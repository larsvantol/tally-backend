from django.urls import path
from rest_framework import routers

from .views import CustomerView, TransactionsView

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = router.urls
urlpatterns += [
    path("transactions/", TransactionsView.as_view(), name="transactions"),
    path("customer/", CustomerView.as_view(), name="customer"),
]
