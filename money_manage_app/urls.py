from django.urls import path

from . import views

app_name = "money_manage_app"

urlpatterns = [
    path("receipt/", views.ReceiptListAPIView.as_view(), name="receipt_list"),
    path(
        "receipt/create/", views.ReceiptCreateAPIView.as_view(), name="receipt_create"
    ),
    path("receipt/<pk>/", views.ReceiptDetailAPIView.as_view(), name="receipt_detail"),
    path("bill/", views.BillListCreateAPIView.as_view(), name="bill_list"),
    path(
        "bill/validate_scan/",
        views.BillValidateScanAPIView.as_view(),
        name="bill_validate_scan",
    ),
    path("bill/<pk>/", views.BillDetailAPIView.as_view(), name="bill_detail"),
    # path("bill/scanned_item/<serial_number>/", views.GetScannedItemsDataForForm.as_view(), name="scanned_item_data"),
]
