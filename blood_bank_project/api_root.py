from django.shortcuts import reverse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response, status


class APIRoot(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        url_dict = {
            "Donation App": {
                "donation_filters": reverse("donation_app:donations_view"),
                "donation_detail": reverse(
                    "donation_app:donation_detail_view", args=["(pk:serial_number)"]
                ),
                "donation_create": reverse("donation_app:donation_create_view"),
                "damage_action": reverse("donation_app:damage_action_view"),
                "test_action": reverse("donation_app:test_action_view"),
                "separation": reverse("donation_app:separation_view"),
                "donors_profiles_list": reverse("donation_app:donors-list"),
                "donors_profiles_detail": reverse(
                    "donation_app:donors-detail", args=["(pk:id)"]
                ),
                "institutes_list": reverse("donation_app:institutes-list"),
                "institutes_detail": reverse(
                    "donation_app:institutes-detail", args=["(pk:id)"]
                ),
                "search": reverse("donation_app:search_view"),
            },
            "Money Manage App": {
                "receipt_list": reverse("money_manage_app:receipt_list"),
                "receipt_detail": reverse(
                    "money_manage_app:receipt_detail", args=["(pk:id)"]
                ),
                "receipt_create": reverse("money_manage_app:receipt_create"),
                "bill_list": reverse("money_manage_app:bill_list"),
                "bill_detail": reverse(
                    "money_manage_app:bill_detail", args=["(pk:id)"]
                ),
                "bill_validate_scan": reverse("money_manage_app:bill_validate_scan"),
                # "scanned_item_data": reverse("money_manage_app:scanned_item_data", args=["serial_number"]),
            },
            "Bank Inventory": {
                "bank_inventory_list": reverse("bank_inventory:bank_inventory_list"),
            },
        }
        return Response(url_dict, status=status.HTTP_200_OK)
