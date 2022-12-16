from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from donation_app.models import (
    InsideDonation, OutsideDonation, ReplaceDonation, DonorProfile, InstituteProfile
)
from donation_app.serializers import (
    InsideDonationSerializer, OutsideDonationSerializer, ReplaceDonationSerializer, DonorProfileSerializer
)
from money_manage_app.models import Receipt
from donation_app import choices
import datetime
from django.utils import timezone
import json


client = Client()


class BankInventoryListTestCase(TestCase):

    #     def test_get_bank_inventory_list(self):
    #         response = client.post(
    #             reverse("bank_inventory:bank_inventory_list"),
    #             {
    #                 "donation_type": "all",
    #                 "unit_type": "all",
    #                 "analyse_status": "all",
    #                 "is_separable": "all"
    #             }
    #         )
    #         print(response.data)
    #         print(data_list)
    #         self.assertEqual(response.data, data_list)
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)

    def setUp(self):
        print("start setUp")

        def get_today():
            return datetime.date.today()

        inside_obj = InsideDonation.objects.create(
            donation_type=choices.INSIDE_DONATION,
            unit_type=choices.FULL_BLOOD,
            blood_type=choices.A_POSITIVE,
            # donation_create_date=datetime.date.today(),
            # donation_create_date=timezone.now().date(),
            # donation_create_date=2022-1-11,
            # donation_create_date=datetime.datetime.now(),
            # donation_create_date='2011-09-01',
            # donation_create_date=datetime.datetime(2020, 5, 17),
            donation_create_date=get_today(),
            donation_expiration_scope=choices.SCOPE_180,
            donor_profile=DonorProfile.objects.create(
                full_name="test_donor",
                age=timezone.now(),
                phone_number="01000000",
                address="Alex",
                national_id="434343434",
                blood_type=choices.DONOR_A_POSITIVE,
                gender=choices.MALE

            )
        )
        outside_obj = OutsideDonation.objects.create(
            donation_type=choices.INSIDE_DONATION,
            unit_type=choices.FULL_BLOOD,
            blood_type=choices.A_POSITIVE,
            donation_create_date=datetime.date.today(),
            donation_expiration_scope=choices.SCOPE_180,
            receipt=Receipt.objects.create(
                hospital_name="test_hospital",
                hospital_phone="0100000000",
                hospital_address="Alex",
                receipt_number=1,
                items_quantity=1
            ),
            general_serial_number="test_general_serial",
        )
        replace_obj = ReplaceDonation.objects.create(
            donation_type=choices.INSIDE_DONATION,
            unit_type=choices.FULL_BLOOD,
            blood_type=choices.A_POSITIVE,
            donation_create_date=datetime.date.today(),
            donation_expiration_scope=choices.SCOPE_180,
            operation_type=choices.IMPORT,
            institute_profile=InstituteProfile.objects.create(
                full_name="test_name",
                phone_number="01000000",
                address="Alex",

            ),
            external_serial_number="external_serial_number",
        )

    def test_get_bank_inventory_list(self):
        z = InsideDonation.objects.get(id=1)
        x = InsideDonationSerializer(z)
        print(x.data)
        response = client.post(
                    reverse("bank_inventory:bank_inventory_list"),
                    data=json.dumps(
                        {
                            "donation_type": ["inside_donation"],
                            "unit_type": ["all"],
                            "analyse_status": ["all"],
                            "is_separable": ["all"]
                        }
                    ),
                    content_type='application/json'
                )
        self.assertEqual(response.status_code, status.HTTP_200_OK)





