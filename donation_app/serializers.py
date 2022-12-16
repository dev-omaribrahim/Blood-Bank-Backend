from django.shortcuts import reverse
from rest_framework import serializers
# from money_manage_app.serializers import ReceiptSerializer
from .models import (
    BaseDonation, InsideDonation, OutsideDonation,
    ReplaceDonation, DonorProfile, InstituteProfile,
    Derivation
)
from . import choices


class DonorProfileSerializer(serializers.ModelSerializer):
    donor_donation_items = serializers.SerializerMethodField()

    def get_donor_donation_items(self, obj):
        donation_items = obj.personal_donation.all()
        serialized_donation_items = DonorProfileInsideDonationSerializer(donation_items, many=True).data
        return serialized_donation_items

    class Meta:
        model = DonorProfile
        fields = "__all__"


class InstituteProfileSerializer(serializers.ModelSerializer):
    institute_items = serializers.SerializerMethodField()

    class Meta:
        model = InstituteProfile
        fields = "__all__"

    def get_institute_items(self, obj):
        response_data = {}
        export_items = obj.replace_institute_donation.filter(
            operation_type=choices.EXPORT
        )
        import_items = obj.replace_institute_donation.filter(
            operation_type=choices.IMPORT
        )
        export_items_data = InstituteReplaceItemsSerializer(export_items, many=True).data
        import_items_data = InstituteReplaceItemsSerializer(import_items, many=True).data
        response_data["export_items"] = export_items_data
        response_data["import_items"] = import_items_data
        response_data["balance"] = export_items.count() - import_items.count()
        return response_data


class InsideDonationSerializer(serializers.ModelSerializer):
    donor_profile = DonorProfileSerializer(read_only=True)
    parents = serializers.SerializerMethodField()

    class Meta:
        model = InsideDonation
        fields = "__all__"
        read_only_fields = ["id", "donor_profile"]

    def get_parents(self, obj):
        objs = obj.parent_derivation.all()
        parents_serial_numbers = [
            reverse(
                "donation_app:donation_detail_view",
                args=[obj.parent.unit_serial_number]
            ) for obj in objs
        ]
        return parents_serial_numbers


class DonorProfileInsideDonationSerializer(serializers.ModelSerializer):
    parents = serializers.SerializerMethodField()

    class Meta:
        model = InsideDonation
        fields = "__all__"
        read_only_fields = ["id", "donor_profile"]

    def get_parents(self, obj):
        objs = obj.parent_derivation.all()
        print(objs)
        parents_serial_numbers = []
        parents_serial_numbers = {
            "data": "no data"
        }
        if objs:
            parents_serial_numbers = [
                reverse(
                    "donation_app:donation_detail_view",
                    args=[obj.parent.unit_serial_number]
                ) for obj in objs if obj.parent.unit_serial_number
            ]
        return parents_serial_numbers


class ReplaceDonationSerializer(serializers.ModelSerializer):
    institute_profile = InstituteProfileSerializer(read_only=True)

    class Meta:
        model = ReplaceDonation
        fields = "__all__"
        # read_only_fields = ["id", "institute_profile"]


class OutsideDonationSerializer(serializers.ModelSerializer):
    from money_manage_app.serializers import ReceiptSerializer  # avoiding circular import
    receipt = ReceiptSerializer(read_only=True)

    class Meta:
        model = OutsideDonation
        fields = "__all__"
        # read_only_fields = ["id", "receipt"]


class InstituteReplaceItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplaceDonation
        fields = "__all__"
        # read_only_fields = ["id", "institute_profile"]


# class AllDonationsInOneSerializer(serializers.Serializer):
#     inside_donation = InsideDonationSerializer(many=True)
#     outside_donation = OutsideDonationSerializer(many=True)
#     replace_donation = ReplaceDonationSerializer(many=True)


from money_manage_app.serializers import ReceiptSerializer
