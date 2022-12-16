from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import AllowAny
from collections import namedtuple
from money_manage_app.models import Receipt
from money_manage_app.serializers import ReceiptSerializer
from donation_app.serializers import (
    InsideDonationSerializer, OutsideDonationSerializer, ReplaceDonationSerializer,
    DonorProfileSerializer, InstituteProfileSerializer
)
from donation_app.models import (
    InsideDonation, OutsideDonation, ReplaceDonation, DonorProfile,
    Derivation, InstituteProfile
)
from donation_app import choices
from .utiles import get_filter_dict


class BankInventoryListAPIView(APIView):
    """
        expected data format from the front end, you can add an item or mare in list or all
            {
                "donation_type": ["inside_donation"] or ["all"],
                "unit_type": ["full_blood"] or ["all"],
                "analyse_status": ["free", "damaged", "pending"] or ["all"],
                "is_separable": ["True", "False"] or ["all"]
            }
    """
    manage_queries = {
        "donation_type": {
            "inside_donation": {
                "model": InsideDonation,
                "serializer": InsideDonationSerializer,
            },
            "outside_donation": {
                "model": OutsideDonation,
                "serializer": OutsideDonationSerializer,
            },
            "replace_donation": {
                "model": ReplaceDonation,
                "serializer": ReplaceDonationSerializer,
            }
        },
    }

    def post(self, request):
        request_data = request.data
        data_list = []

        if {"donation_type", "unit_type", "analyse_status", "is_separable"} <= request.data.keys():

            filter_dict = get_filter_dict(request_data)
            if request_data["donation_type"] == ["all"]:
                request_data["donation_type"] = ["inside_donation", "outside_donation", "replace_donation"]

            for key in request_data["donation_type"]:
                if not filter_dict:
                    query = self.manage_queries["donation_type"][key]["model"].objects.all()
                else:
                    query = self.manage_queries["donation_type"][key]["model"].objects.filter(**filter_dict)

                if key == choices.REPLACE_DONATION:
                    query.exclude(operation_type=choices.EXPORT)

                serializer = self.manage_queries["donation_type"][key]["serializer"]
                data = serializer(query, many=True).data
                data_list += data

            return Response(data_list, status=status.HTTP_200_OK)
        else:
            return Response("Please Provide The Required Data !", status=status.HTTP_400_BAD_REQUEST)


class DonationFilterAPIView(APIView):
    """
    this is for filter specific donation type
    data format required:
    {
        "filter_in": "inside_donation" / "outside_donation" / "replace_donation",
        "filter_value": for inside_donation is: blood_type
    }
    """

    def get(self, request, *args, **kwargs):
        if {"filter_in", "filter_value"} <= request.data:
            request_data = request.data
            if request_data["filter_in"] == "inside_donation":
                objs = InsideDonation.objects.filter(
                    blood_type=request_data["filter_value"]
                )
                objs_serializer = InsideDonationSerializer(objs, many=True)
                return Response(objs_serializer.data, status=status.HTTP_200_OK)
            elif request_data["filter_in"] == "outside_donation":
                pass
            elif request_data["filter_in"] == "replace_donation":
                pass
            else:
                return Response("Invalid filter_in data !", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Provide Required Data !", status=status.HTTP_400_BAD_REQUEST)