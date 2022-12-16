import datetime

from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from donation_app.models import (
    InsideDonation, OutsideDonation, ReplaceDonation
)
from donation_app.serializers import (
    InsideDonationSerializer, OutsideDonationSerializer,
    ReplaceDonationSerializer,
)
from donation_app import choices
from .serializers import ReceiptSerializer, BillSerializer
from .models import Receipt, Bill, Prices
from .utils import convert_to_blood_group


class ReceiptListAPIView(APIView):

    def get(self, request):
        all_receipts = Receipt.objects.all()
        all_receipts_data = ReceiptSerializer(all_receipts, many=True)
        return Response(all_receipts_data.data)


class ReceiptDetailAPIView(APIView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]

        try:
            receipt = Receipt.objects.get(id=pk)
        except Receipt.DoesNotExist:
            return Response("Receipt Not Found !", status=status.HTTP_204_NO_CONTENT)

        receipt = ReceiptSerializer(receipt)
        return Response(receipt.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            receipt = Receipt.objects.get(id=pk)
        except Receipt.DoesNotExist:
            return Response("Receipt Not Found !", status=status.HTTP_204_NO_CONTENT)
        receipt_serializer = ReceiptSerializer(receipt, data=request.data)
        if receipt_serializer.is_valid():
            receipt_serializer.save()
            return Response(receipt_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(receipt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]

        try:
            receipt = Receipt.objects.get(id=pk)
        except Receipt.DoesNotExist:
            return Response("Receipt Not Found !", status=status.HTTP_204_NO_CONTENT)
        receipt_data = ReceiptSerializer(receipt).data
        receipt.delete()
        return Response(receipt_data, status=status.HTTP_200_OK)


class ReceiptCreateAPIView(APIView):

    def post(self, request):
        request_data = request.data
        new_receipt = ReceiptSerializer(data=request_data)
        if new_receipt.is_valid():
            new_receipt.save()
            return Response(new_receipt.data, status=status.HTTP_200_OK)
        else:
            return Response(new_receipt.errors, status=status.HTTP_400_BAD_REQUEST)


class BillListCreateAPIView(APIView):
    """
    this view is for lit and create bill objects
    get: will return list of bills
    post: will create a bill with its items
    create via post requires data format as follow:
    {
        "customer_data": {
            "bill_name": "new bill 1",
            "blood_type": "a_positive",
            "patient_name": "man 1",
            "patient_gender": "male",
            "patient_age": "1990-5-5",
            "hospital_name": "al nahar 2",
            "patient_national_id": "8552147"
        },
        "blood_bag_serial_numbers":["outside_donation-738376", "inside_donation-648528"],
        "prices": ["344.22", "444.05", "333.00"]
    }
    """
    def get(self, request, *args, **kwargs):
        objs = Bill.objects.all()
        objs_serializer = BillSerializer(objs, many=True)
        return Response(objs_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        donation_type_manager = {
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
        }
        if {"customer_data", "blood_bag_serial_numbers", "prices"} <= request.data.keys():
            request_data = request.data
            obj_serializer = BillSerializer(data=request_data["customer_data"])

            if obj_serializer.is_valid():
                total_price = sum(float(n) for n in request_data["prices"])
                bill = obj_serializer.save(total_price=total_price)
                for serial in request_data["blood_bag_serial_numbers"]:
                    donation_type = serial.split("-")[0]
                    try:
                        obj = donation_type_manager[donation_type]["model"].objects.get(unit_serial_number=serial)
                    except donation_type_manager[donation_type]["model"].DoesNotExist:
                        return Response("Not Found !", status=status.HTTP_204_NO_CONTENT)

                    obj.unit_bill = bill
                    obj.is_sold = True
                    obj.save()

                return Response("Created Successfully", status=status.HTTP_201_CREATED)
            else:
                return Response(obj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("Provide Required Data", status=status.HTTP_400_BAD_REQUEST)


class BillDetailAPIView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            try:
                bill = Bill.objects.get(pk=pk)
            except Bill.DoesNotExist:
                return Response("Not Found !", status=status.HTTP_204_NO_CONTENT)
            bill_serializer = BillSerializer(bill)
            return Response(bill_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Provide PK !", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            try:
                bill = Bill.objects.get(pk=pk)
            except Bill.DoesNotExist:
                return Response("Not Found !", status=status.HTTP_204_NO_CONTENT)

            bill_serializer = BillSerializer(bill, data=request.data)
            if bill_serializer.is_valid():
                bill_serializer.save()
                return Response("Updated Successfully", status=status.HTTP_200_OK)
            else:
                return Response(bill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Provide PK !", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            try:
                bill = Bill.objects.get(pk=pk)
            except Bill.DoesNotExist:
                return Response("Not Found !", status=status.HTTP_204_NO_CONTENT)
            bill_data = BillSerializer(bill).data
            bill.delete()
            return Response(bill_data, status=status.HTTP_200_OK)
        else:
            return Response("Provide PK !", status=status.HTTP_400_BAD_REQUEST)


class BillValidateScanAPIView(APIView):
    """
    this view is for checking every item based on the given condition in requirement doc
    added to bill via serial number scan.
    it return serial number / unit type / unit price, or raise an error
    data format as follow:
    {
        "customer_data": {
            "blood_type": "a_positive"
        },
        "blood_bag_data": {
            "serial_number": "inside_donation-648528"
        }
    }
    """
    donation_type_manager = {
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
    }

    def post(self, request, *args, **kwargs):
        if {"customer_data", "blood_bag_data"} <= request.data.keys():
            request_data = request.data
            donation_type = request_data["blood_bag_data"]["serial_number"].split("-")[0]

            if donation_type not in self.donation_type_manager.keys():
                return Response("Obj Not Found !", status=status.HTTP_400_BAD_REQUEST)

            obj_model = self.donation_type_manager[donation_type]["model"]
            obj_serializer = self.donation_type_manager[donation_type]["serializer"]

            try:
                obj = obj_model.objects.get(unit_serial_number=request_data["blood_bag_data"]["serial_number"])
            except obj_model.DoesNotExist:
                return Response("Obj Not Found !", status=status.HTTP_400_BAD_REQUEST)

            patient_blood_type = request_data["customer_data"]["blood_type"]
            patient_blood_group = convert_to_blood_group(request_data["customer_data"]["blood_type"])

            obj_blood_type = obj.blood_type
            obj_blood_group = convert_to_blood_group(obj.blood_type)

            if (obj.unit_type in [choices.FULL_BLOOD, choices.RBCs] and obj_blood_type != patient_blood_type) or \
                    (obj.unit_type in [choices.PLASMA, choices.CRYO, choices.BLOOD_PLATELETS] and obj_blood_group != patient_blood_group):

                return Response("Not the same blood type !", status=status.HTTP_400_BAD_REQUEST)

            if obj.analyse_status == choices.PENDING or obj.analyse_status == choices.DAMAGED:
                return Response("This item is Pending or Damaged !", status=status.HTTP_400_BAD_REQUEST)

            if obj.donation_expire_date <= datetime.date.today():
                return Response("This item will expire today or it is already expired !", status=status.HTTP_400_BAD_REQUEST)

            try:
                obj_price = Prices.objects.get(unit_type=obj.unit_type)
            except Prices.DoesNotExist:
                obj_price = None
            data = {
                "serial_number": obj.unit_serial_number,
                "unit_type": obj.unit_type,
                "unit_price": obj_price.unit_price
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response("Provide Required Data", status=status.HTTP_400_BAD_REQUEST)
