from rest_framework import serializers

from donation_app.models import InsideDonation, OutsideDonation, ReplaceDonation

from . import models


class ReceiptSerializer(serializers.ModelSerializer):
    receipt_items = serializers.SerializerMethodField()

    class Meta:
        model = models.Receipt
        fields = "__all__"

    def get_receipt_items(self, obj):
        items = obj.donated_units.all()
        items_data = ReplaceDonationSerializer(items, many=True).data
        return items_data


class BillSerializer(serializers.ModelSerializer):
    bill_items = serializers.SerializerMethodField()

    class Meta:
        model = models.Bill
        fields = "__all__"

    def get_bill_items(self, obj):
        inside_donations = InsideDonation.objects.filter(unit_bill=obj)
        outside_donations = OutsideDonation.objects.filter(unit_bill=obj)
        replace_donations = ReplaceDonation.objects.filter(unit_bill=obj)
        serialized_data = []
        if inside_donations:
            q = InsideDonationSerializer(inside_donations, many=True).data
            serialized_data += q
        if outside_donations:
            q = OutsideDonationSerializer(outside_donations, many=True).data
            serialized_data += q
        if replace_donations:
            q = ReplaceDonationSerializer(replace_donations, many=True).data
            serialized_data += q
        return serialized_data


# avoiding circular error
from donation_app.serializers import (
    InsideDonationSerializer,
    OutsideDonationSerializer,
    ReplaceDonationSerializer,
)
