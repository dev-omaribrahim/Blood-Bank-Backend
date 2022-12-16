"""blood_bank_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from .api_root import APIRoot

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("custom_authentication.urls")),
    path("api/v1/donations/", include("donation_app.urls")),
    path("api/v1/manage_purchases/", include("money_manage_app.urls")),
    path("api/v1/bank_inventory/", include("bank_inventory_app.urls")),
    path("api/v1/root/", APIRoot.as_view(), name="api_root"),
]
