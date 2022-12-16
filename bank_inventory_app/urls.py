from django.urls import path
from . import views


app_name = "bank_inventory"


urlpatterns = [
    path("", views.BankInventoryListAPIView.as_view(), name="bank_inventory_list"),
]