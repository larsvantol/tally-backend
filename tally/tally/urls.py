"""tally URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import products.urls as products_urls
import transactions.urls as transactions_urls
from django.contrib import admin
from django.urls import include, path

from .views import is_authenticatedView, login_failureView, loginView, logoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("settings/", include("dbsettings.urls")),
    path("products/", include((products_urls.router.urls, "products"))),
    path("transactions/", include((transactions_urls.router.urls, "transactions"))),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("auth/is_authenticated/", is_authenticatedView, name="is_authenticated"),
    path("auth/login/", loginView, name="login"),
    path("auth/logout/", logoutView, name="logout"),
    path("auth/login_failure/", login_failureView, name="login_failure"),
]
