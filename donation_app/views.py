from collections import namedtuple

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response, status

from money_manage_app.models import Receipt
from money_manage_app.serializers import ReceiptSerializer

from . import choices
from .models import (
    Derivation,
    DonorProfile,
    InsideDonation,
    InstituteProfile,
    OutsideDonation,
    ReplaceDonation,
)
from .serializers import (
    DonorProfileSerializer,
    InsideDonationSerializer,
    InstituteProfileSerializer,
    OutsideDonationSerializer,
    ReplaceDonationSerializer,
)

# class DonationsView(APIView):
#     """
#     this view is for filters it work with one filter select,
#     it will be edited due to change one filter => multi filter
#     """
#     permission_classes = (AllowAny,)
#     manage_queries = {
#         "donation_type": {
#             "inside_donation": {
#                 "model": InsideDonation,
#                 "serializer": InsideDonationSerializer,
#             },
#             "outside_donation": {
#                 "model": OutsideDonation,
#                 "serializer": OutsideDonationSerializer,
#             },
#             "replace_donation": {
#                 "model": ReplaceDonation,
#                 "serializer": ReplaceDonationSerializer,
#             }
#         },
#         "unit_type": {
#             "full_blood": "full_blood",
#             "RBCs": "rbcs",
#             "blood_platelets": "blood_platelets",
#             "plasma": "plasma",
#             "cryo": "cryo",
#         },
#         "is_separable": {
#             "true": True,
#             "false": False,
#         }
#     }
#
#     def get(self, request):
#         request_data = request.data
#
#         if request_data["donation_type"] == "all":
#
#             if request_data["unit_type"] == "all":
#                 Donation = namedtuple('Donations', ('inside_donation', 'outside_donation', 'replace_donation'))
#                 queries = Donation(
#                     inside_donation=InsideDonation.objects.all(),
#                     outside_donation=OutsideDonation.objects.all(),
#                     replace_donation=ReplaceDonation.objects.all(),
#                 )
#                 serializer = AllDonationsInOneSerializer(queries)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 Donation = namedtuple('Donations', ('inside_donation', 'outside_donation', 'replace_donation'))
#                 queries = Donation(
#                     inside_donation=InsideDonation.objects.filter(
#                         unit_type=self.manage_queries["unit_type"][request_data["unit_type"]]
#                     ),
#                     outside_donation=OutsideDonation.objects.filter(
#                         unit_type=self.manage_queries["unit_type"][request_data["unit_type"]]
#                     ),
#                     replace_donation=ReplaceDonation.objects.filter(
#                         unit_type=self.manage_queries["unit_type"][request_data["unit_type"]]
#                     ),
#                 )
#                 serializer = AllDonationsInOneSerializer(queries)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#
#         elif request_data["donation_type"] != "all":
#
#             if request_data["unit_type"] == "all":
#                 query = self.manage_queries["donation_type"][request_data["donation_type"]]["model"].objects.all()
#                 model_serializer = self.manage_queries["donation_type"][request_data["donation_type"]]["serializer"]
#                 serializer = model_serializer(query, many=True)
#                 return Response(serializer.data)
#             else:
#                 query = self.manage_queries["donation_type"][request_data["donation_type"]]["model"].objects.filter(
#                     unit_type=request_data["unit_type"]
#                 )
#                 model_serializer = self.manage_queries["donation_type"][request_data["donation_type"]]["serializer"]
#                 serializer = model_serializer(query, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#
#         else:
#             return Response("There is a problem", status=status.HTTP_400_BAD_REQUEST)


class SeparationAPIView(APIView):
    """
    This view class is used for separating and create derivatives:
    full blood => plasma, and the full blood become RBCs
    plasma => cryo and blood platelets
    for inside donations only
    {
        "parent_serial_number": inside_donation-273462,
        "type_of_derivative_unit": "plasma" / "blood_platelets" / "cryo",
        "donation_expiration_scope": 35,
    }
    """

    def post(self, request):

        if {
            "parent_serial_number",
            "type_of_derivative_unit",
            "donation_expiration_scope",
        } <= request.data.keys():
            # get the data from front-end
            # expected data is (parent_id) and (type_of_derivative_unit)
            request_data = request.data

            # get the parent object that we will drive form it
            # and copy its data if exist or return an error message
            try:
                parent_obj = InsideDonation.objects.get(
                    unit_serial_number=request_data["parent_serial_number"]
                )
            except InsideDonation.DoesNotExist:
                return Response("Object Not Found!", status=status.HTTP_404_NOT_FOUND)

            # if the desired unit is plasma then check if the parent is full blood
            # and didn't separated before if so then create the unit
            if (
                request_data["type_of_derivative_unit"] == choices.PLASMA
                and parent_obj.unit_type == choices.FULL_BLOOD
                and parent_obj.is_separable
            ):

                new_child_obj = InsideDonation.objects.create(
                    donation_type=parent_obj.donation_type,
                    unit_type=choices.PLASMA,
                    blood_type=parent_obj.blood_type,
                    donation_create_date=parent_obj.donation_create_date,
                    donation_expiration_scope=request_data["donation_expiration_scope"],
                    donor_profile=DonorProfile.objects.get(
                        id=parent_obj.donor_profile.id
                    ),
                    is_derivative=True,
                )
                Derivation.objects.create(
                    parent=parent_obj,
                    child=new_child_obj,
                )
                parent_obj.used_for_deriving = True
                parent_obj.unit_type = choices.RBCs
                parent_obj.save()

                response_data = {
                    "parent": InsideDonationSerializer(parent_obj).data,
                    "child": InsideDonationSerializer(new_child_obj).data,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            # if the desired unit is blood platelets then check if the parent is plasma
            # and didn't separated before if so then create the unit
            elif (
                request_data["type_of_derivative_unit"] == choices.BLOOD_PLATELETS
                and parent_obj.unit_type == choices.PLASMA
                and parent_obj.is_separable
            ):

                new_child_obj = InsideDonation.objects.create(
                    donation_type=parent_obj.donation_type,
                    unit_type=choices.BLOOD_PLATELETS,
                    blood_type=parent_obj.blood_type,
                    donation_create_date=parent_obj.donation_create_date,
                    donation_expiration_scope=request_data["donation_expiration_scope"],
                    donor_profile=DonorProfile.objects.get(
                        id=parent_obj.donor_profile.id
                    ),
                    is_derivative=True,
                )
                Derivation.objects.create(
                    parent=parent_obj,
                    child=new_child_obj,
                )
                parent_obj.used_for_deriving = True
                parent_obj.save()

                response_data = {
                    "parent": InsideDonationSerializer(parent_obj).data,
                    "child": InsideDonationSerializer(new_child_obj).data,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            # if the desired unit is blood cryo then check if the parent is plasma
            # and didn't separated before if so then create the unit
            elif (
                request_data["type_of_derivative_unit"] == choices.CRYO
                and parent_obj.unit_type == choices.PLASMA
                and parent_obj.is_separable
            ):

                new_child_obj = InsideDonation.objects.create(
                    donation_type=parent_obj.donation_type,
                    unit_type=choices.CRYO,
                    blood_type=parent_obj.blood_type,
                    donation_create_date=parent_obj.donation_create_date,
                    donation_expiration_scope=request_data["donation_expiration_scope"],
                    donor_profile=DonorProfile.objects.get(
                        id=parent_obj.donor_profile.id
                    ),
                    is_derivative=True,
                )
                Derivation.objects.create(
                    parent=parent_obj,
                    child=new_child_obj,
                )
                parent_obj.used_for_deriving = True
                parent_obj.save()

                response_data = {
                    "parent": InsideDonationSerializer(parent_obj).data,
                    "child": InsideDonationSerializer(new_child_obj).data,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response("separation failed", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "Provide Required Data !", status=status.HTTP_400_BAD_REQUEST
            )


class OldDonationCreateAPIView(APIView):
    def post(self, request):

        if {
            "donation_type",
            "donator_profile_id",
            "donation_data",
        } <= request.data.keys():
            request_data = request.data

            if request_data["donation_type"] == choices.INSIDE_DONATION:

                try:
                    donor_profile = DonorProfile.objects.get(
                        pk=request_data["donator_profile_id"]
                    )
                except DonorProfile.DoesNotExist:
                    return Response("Not Found !", status=status.HTTP_204_NO_CONTENT)

                donation_serializer = InsideDonationSerializer(
                    data=request_data["donation_data"]
                )

                if donation_serializer.is_valid():
                    donation_serializer.save(donor_profile=donor_profile)
                    return Response(
                        donation_serializer.data, status=status.HTTP_201_CREATED
                    )

                return Response(
                    donation_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            elif request_data["donation_type"] == choices.OUTSIDE_DONATION:

                try:
                    receipt = Receipt.objects.get(
                        receipt_number=request_data["donator_profile_id"]
                    )
                except Receipt.DoesNotExist:
                    return Response(
                        "Object Not Found !", status=status.HTTP_204_NO_CONTENT
                    )

                outside_donation_serializer = OutsideDonationSerializer(
                    data=request_data["donation_data"]
                )
                if outside_donation_serializer.is_valid():
                    outside_donation_serializer.save(receipt=receipt)
                    return Response(
                        outside_donation_serializer.data, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        outside_donation_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            elif request_data["donation_type"] == choices.REPLACE_DONATION:
                try:
                    institute = InstituteProfile.objects.get(
                        id=request_data["donator_profile_id"]
                    )
                except InstituteProfile.DoesNotExist:
                    return Response("Not Found !", status=status.HTTP_204_NO_CONTENT)
                replace_donation_serializer = ReplaceDonationSerializer(
                    data=request_data["donation_data"]
                )
                if replace_donation_serializer.is_valid():
                    replace_donation_serializer.save(institute_profile=institute)
                    return Response(
                        replace_donation_serializer.data, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        replace_donation_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    "Creation Failed, Invalid donation_data !",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                "Provide Required Data !", status=status.HTTP_400_BAD_REQUEST
            )


class DonationCreateAPIView(APIView):
    """
    if the donator profile (donor_profile / receipt / institute) exist. data format as follow:
    {
            "donation_type": "outside_donation" / "inside_donation" / "replace_donation",
            "donator_profile_data": {
                "id": 1,
            },
            "donation_data": [
                {
                    donation item 1
                },
                {
                    donation item 2
                }
            ]
        }
    if the donator profile (donor_profile / receipt / institute) not exist. data format as follow:
        {
            "donation_type": "outside_donation" / "inside_donation" / "replace_donation",
            "donator_profile_data": {
                "id": 1,
                "hospital_name": "el nahar",
                "hospital_general_serial_number": "878787",
                "receipt_number": 4324,
                "receipt_date": "2021-12-20",
                "items_quantity": 2
            },
            "donation_data": [
                {
                    donation item 1
                },
                {
                    donation item 2
                }
            ]
        }
    """

    def post(self, request):

        # check if request contain required data or raise an error
        if {
            "donation_type",
            "donator_profile_data",
            "donation_data",
        } <= request.data.keys():
            # get request data
            request_data = request.data

            # create inside donation
            if request_data["donation_type"] == choices.INSIDE_DONATION:
                # append all serialized items in the response data to return it to
                # the frontend
                response_data = []

                # this dict is for storing data about the donator so i can use it to manage
                # whether i delete if some error happen or leave it
                donator_dic = {"donator_is_new": None, "donator_items_ids": []}

                # try to get the donator profile if it exist process with it or create a new one
                try:
                    donor_profile = DonorProfile.objects.get(
                        pk=request_data["donator_profile_data"]["id"]
                    )
                    # mark the donator profile as old
                    donator_dic["donator_is_new"] = False
                except Exception:
                    donor_profile_serializer = DonorProfileSerializer(
                        data=request_data["donator_profile_data"]
                    )
                    if donor_profile_serializer.is_valid():
                        donor_profile = donor_profile_serializer.save()
                        # mark the donator profile as new
                        donator_dic["donator_is_new"] = True
                    else:
                        return Response(
                            donor_profile_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # processed with creating the items if the donator is valid
                for item in request_data["donation_data"]:

                    donation_serializer = InsideDonationSerializer(data=item)
                    if donation_serializer.is_valid():
                        donation_serializer.save(donor_profile=donor_profile)
                        # when the item is created append its id to institute_dict so i can delete it
                        # if needed later
                        donator_dic["donator_items_ids"].append(
                            donation_serializer.data["id"]
                        )
                        # append the serializer data to response data to return the items to frontend
                        response_data.append(donation_serializer.data)
                    else:
                        # if the item is not valid the following process is for deleting all created data above
                        # if the donator profile is new then delete it with its created items
                        # if the donator profile is old then just delete the created items above
                        if donator_dic["donator_is_new"] == True:
                            errors = donation_serializer.errors
                            donor_profile.personal_donation.filter(
                                id__in=donator_dic["donator_items_ids"]
                            ).delete()
                            donor_profile.delete()
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            errors = donation_serializer.errors
                            donor_profile.personal_donation.filter(
                                id__in=donator_dic["donator_items_ids"]
                            ).delete()
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(response_data, status=status.HTTP_201_CREATED)

            # create outside donation
            elif request_data["donation_type"] == choices.OUTSIDE_DONATION:
                # append all serialized items in the response data to return it to
                # the frontend
                response_data = []

                # this dict is for storing data about the institute so i can use it to manage
                # whether i delete if some error happen or leave it
                donator_dic = {"donator_is_new": None, "donator_items_ids": []}

                # try to get the donator profile if it exist process with it or create a new one
                try:
                    receipt = Receipt.objects.get(
                        receipt_number=request_data["donator_profile_data"]["id"]
                    )
                    # mark the donator profile as old
                    donator_dic["donator_is_new"] = False
                except Exception:
                    receipt_serializer = ReceiptSerializer(
                        data=request_data["donator_profile_data"]
                    )
                    if receipt_serializer.is_valid():
                        receipt = receipt_serializer.save()
                        # mark the donator profile as new
                        donator_dic["donator_is_new"] = True
                        print("valid")
                    else:
                        print("not valid")
                        return Response(
                            receipt_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # processed with creating the items if the donator is valid
                for item in request_data["donation_data"]:
                    outside_donation_serializer = OutsideDonationSerializer(data=item)
                    if outside_donation_serializer.is_valid():
                        outside_donation_serializer.save(receipt=receipt)
                        # when the item is created append its id to institute_dict so i can delete it
                        # if needed later
                        donator_dic["donator_items_ids"].append(
                            outside_donation_serializer.data["id"]
                        )
                        # append the serializer data to response data to return the items to frontend
                        response_data.append(outside_donation_serializer.data)
                    else:
                        # if the item is not valid the following process is for deleting all created data above
                        # if the donator profile is new then delete it with its created items
                        # if the donator profile is old then just delete the created items above
                        if donator_dic["donator_is_new"] == True:
                            errors = outside_donation_serializer.errors
                            receipt.donated_units.filter(
                                id__in=donator_dic["donator_items_ids"]
                            ).delete()
                            receipt.delete()
                            print("new deleted")
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            errors = outside_donation_serializer.errors
                            receipt.donated_units.filter(
                                id__in=donator_dic["donator_items_ids"]
                            ).delete()
                            print("old deleted")
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(response_data, status=status.HTTP_201_CREATED)

            # create replace donation
            elif request_data["donation_type"] == choices.REPLACE_DONATION:

                # append all serialized items in the response data to return it to
                # the frontend
                response_data = []

                # this dict is for storing data about the institute so i can use it to manage
                # whether i delete if some error happen or leave it
                donator_dic = {"donator_is_new": None, "donator_items_ids": []}

                try:
                    institute = InstituteProfile.objects.get(
                        id=request_data["donator_profile_data"]["id"]
                    )
                    # mark the donator profile as old
                    donator_dic["donator_is_new"] = False
                except Exception:
                    institute_serializer = InstituteProfileSerializer(
                        data=request_data["donator_profile_data"]
                    )
                    if institute_serializer.is_valid():
                        institute = institute_serializer.save()
                        # mark the donator profile as new
                        donator_dic["donator_is_new"] = True
                    else:
                        return Response(
                            institute_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # processed with creating the items if the donator is valid
                for item in request_data["donation_data"]:
                    replace_donation_serializer = ReplaceDonationSerializer(data=item)
                    if replace_donation_serializer.is_valid():
                        replace_donation_serializer.save(institute_profile=institute)
                        # when the item is created append its id to institute_dict so i can delete it
                        # if needed later
                        donator_dic["donator_items_ids"].append(
                            replace_donation_serializer.data["id"]
                        )
                        # append the serializer data to response data to return the items to frontend
                        response_data.append(replace_donation_serializer.data)
                    else:
                        # if the item is not valid the following process is for deleting all created data above
                        # if the donator profile is new then delete it with its created items
                        # if the donator profile is old then just delete the created items above
                        if donator_dic["donator_is_new"] == True:
                            errors = replace_donation_serializer.errors
                            institute.replace_institute_donation.filter(
                                id__in=donator_dic["donator_items_ids"]
                            ).delete()
                            institute.delete()
                            print("new deleted")
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            errors = replace_donation_serializer.errors
                            institute.replace_institute_donation.filter(
                                id__in=donator_dic["donator_items_ids"]
                            ).delete()
                            print("old deleted")
                            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(response_data, status=status.HTTP_201_CREATED)

            else:
                return Response(
                    "Creation Failed, Invalid donation_data !",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                "Provide Required Data !", status=status.HTTP_400_BAD_REQUEST
            )


class DonationDetailAPIView(APIView):
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
        },
    }

    def get(self, request, *args, **kwargs):
        serial_number = kwargs.get("serial_number", None)
        if serial_number:
            donation_type_url = serial_number.split("-")[0]
            print(self.donation_type_manager[donation_type_url])
            obj_model = self.donation_type_manager[donation_type_url]["model"]
            obj_serializer = self.donation_type_manager[donation_type_url]["serializer"]
            try:
                obj = obj_model.objects.get(unit_serial_number=serial_number)
            except obj_model.DoesNotExist:
                return Response("Obj Not Found !", status=status.HTTP_204_NO_CONTENT)
            return Response(obj_serializer(obj).data, status=status.HTTP_200_OK)
        else:
            return Response("Provide Required PK !", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        serial_number = kwargs.get("serial_number", None)
        if serial_number:
            donation_type_url = serial_number.split("-")[0]
            print(self.donation_type_manager[donation_type_url])
            obj_model = self.donation_type_manager[donation_type_url]["model"]
            obj_serializer = self.donation_type_manager[donation_type_url]["serializer"]
            try:
                obj = obj_model.objects.get(unit_serial_number=serial_number)
            except obj_model.DoesNotExist:
                return Response("Obj Not Found !", status=status.HTTP_204_NO_CONTENT)
            serializer_data = obj_serializer(obj, data=request.data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response(obj_serializer(obj).data, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer_data.errors, status=status.HTTP_400_BAD_REQUEST
                )

    def delete(self, request, *args, **kwargs):
        serial_number = kwargs.get("serial_number", None)
        if serial_number:
            donation_type_url = serial_number.split("-")[0]
            # print(self.donation_type_manager[donation_type_url])
            obj_model = self.donation_type_manager[donation_type_url]["model"]
            obj_serializer = self.donation_type_manager[donation_type_url]["serializer"]
            try:
                obj = obj_model.objects.get(unit_serial_number=serial_number)
            except obj_model.DoesNotExist:
                return Response("Obj Not Found !", status=status.HTTP_204_NO_CONTENT)
            obj_data = obj_serializer(obj).data
            obj.delete()
            return Response(obj_data, status=status.HTTP_200_OK)
        else:
            return Response("Provide Required PK !", status=status.HTTP_400_BAD_REQUEST)


class DamageActionAPIView(APIView):
    """
    This view is for Damage action, required data:
    in case of damaging the unit:
    {
        "donation_type": "inside_donation",
        "serial_number": "inside_donation-273462",
        "action_details": {
            "action_type": "do_damage",
            "reason": "place_holder1" / "place_holder2"
        }
    }
    in case of undo damage:
    {
        "donation_type": "inside_donation",
        "serial_number": "inside_donation-273462",
        "action_details": {
            "action_type": "undo_damage",
            "analyse_status": "free" / "pending"
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
        },
    }

    def post(self, request, *args, **kwargs):

        if {"donation_type", "serial_number", "action_details"} <= request.data.keys():
            request_data = request.data
            obj_model = self.donation_type_manager[request_data["donation_type"]][
                "model"
            ]
            obj_serializer = self.donation_type_manager[request_data["donation_type"]][
                "serializer"
            ]

            try:
                obj = obj_model.objects.get(
                    unit_serial_number=request_data["serial_number"]
                )
            except obj_model.DoesNotExist:
                return Response(
                    "Object Not Found !", status=status.HTTP_400_BAD_REQUEST
                )

            if request_data["action_details"]["action_type"] == "do_damage":
                obj.analyse_status = choices.DAMAGED
                obj.unit_notes = request_data["action_details"]["reason"]
                obj.save()
                return Response(obj_serializer(obj).data, status=status.HTTP_200_OK)

            elif request_data["action_details"]["action_type"] == "undo_damage":
                obj.analyse_status = request_data["action_details"]["analyse_status"]
                obj.save()
                return Response(obj_serializer(obj).data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "Provide a Valid Action !", status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                "Provide Required Data !", status=status.HTTP_400_BAD_REQUEST
            )


class TestActionAPIView(APIView):
    """
    This view is for Test action (passed or failed), required data:
    {
        "donation_type": "inside_donation" / "outside_donation" / "replace_donation",
        "serial_number": "the serial number of the unit",
        "action": "test_passed" / "test_failed"
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
        },
    }

    def post(self, request, *args, **kwargs):

        if {"donation_type", "serial_number", "action"} <= request.data.keys():
            request_data = request.data
            obj_model = self.donation_type_manager[request_data["donation_type"]][
                "model"
            ]
            obj_serializer = self.donation_type_manager[request_data["donation_type"]][
                "serializer"
            ]
            try:
                obj = obj_model.objects.get(
                    unit_serial_number=request_data["serial_number"]
                )
            except obj_model.DoesNotExist:
                return Response(
                    "Object Not Found !", status=status.HTTP_400_BAD_REQUEST
                )
            if request_data["action"] == "test_failed":
                obj.analyse_status = choices.DAMAGED
                obj.save()
                return Response(obj_serializer(obj).data, status=status.HTTP_200_OK)
            elif request_data["action"] == "test_passed":
                obj.analyse_status = choices.FREE
                obj.save()
                return Response(obj_serializer(obj).data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "Provide a Valid Action !", status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                "Provide Required Data !", status=status.HTTP_400_BAD_REQUEST
            )


class SearchAPIView(APIView):
    """
    Search View Expect data via get request in format:
    {
        "search_in": inside_donation, outside_donation, replace_donation, donor_profile or
        institute_profile,
        "search_keyword": serial_number for donations, national_id or full_name for donor profile,
         name for institute
    }
    """

    def get(self, request, *args, **kwargs):
        request_data = request.data
        # check if request data contains the desired data or return
        # provide required data
        if {"search_in", "search_keyword"} <= request.data.keys():

            # if branch to handle many 'search in' places
            if request_data["search_in"] == "inside_donation":
                try:
                    obj = InsideDonation.objects.get(
                        unit_serial_number=request_data["search_keyword"]
                    )
                except InsideDonation.DoesNotExist:
                    return Response(
                        "Donation Not Found. Note: Search Via Serial number",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # objs = InsideDonation.objects.filter(unit_serial_number__icontains=request_data["search_keyword"])
                # obj_serializer = InsideDonationSerializer(objs, many=True)
                obj_serializer = InsideDonationSerializer(obj)
                return Response(obj_serializer.data, status=status.HTTP_200_OK)

            elif request_data["search_in"] == "outside_donation":
                try:
                    obj = OutsideDonation.objects.get(
                        unit_serial_number=request_data["search_keyword"]
                    )
                except OutsideDonation.DoesNotExist:
                    return Response(
                        "Donation Not Found. Note: Search Via Serial number",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                obj_serializer = OutsideDonationSerializer(obj)
                return Response(obj_serializer.data, status=status.HTTP_200_OK)

            elif request_data["search_in"] == "replace_donation":
                try:
                    obj = ReplaceDonation.objects.get(
                        unit_serial_number=request_data["search_keyword"]
                    )
                except ReplaceDonation.DoesNotExist:
                    return Response(
                        "Donation Not Found. Note: Search Via Serial number",
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                obj_serializer = ReplaceDonationSerializer(obj)
                return Response(obj_serializer.data, status=status.HTTP_200_OK)

            elif request_data["search_in"] == "donor_profile":

                try:
                    # here obj may show an error due to wrong data format entered by user
                    # but, it handeled
                    obj = DonorProfile.objects.get(
                        national_id=int(request_data["search_keyword"])
                    )
                    obj_serializer = DonorProfileSerializer(obj)
                except Exception:
                    obj = DonorProfile.objects.filter(
                        full_name=request_data["search_keyword"]
                    )
                    obj_serializer = DonorProfileSerializer(obj, many=True)

                return Response(obj_serializer.data, status=status.HTTP_200_OK)

            elif request_data["search_in"] == "institute_profile":
                obj = InstituteProfile.objects.filter(
                    full_name=request_data["search_keyword"]
                )
                obj_serializer = InstituteProfileSerializer(obj, many=True)
                return Response(obj_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "Unsupported Search Type !", status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                "Please Provide Required Data !", status=status.HTTP_400_BAD_REQUEST
            )


class DonorProfileViewSet(viewsets.ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj_data = DonorProfileSerializer(obj).data
        obj.delete()
        return Response(obj_data, status=status.HTTP_200_OK)


class InstituteProfileViewSet(viewsets.ModelViewSet):
    queryset = InstituteProfile.objects.all()
    serializer_class = InstituteProfileSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj_data = InstituteProfileSerializer(obj).data
        obj.delete()
        return Response(obj_data, status=status.HTTP_200_OK)


class MultiFilterAPIView(APIView):
    """
    expected data format from the front end
        {
            "donation_type": ["inside_donation", "outside_donation", "replace_donation"],
            "unit_type_list": ["full_blood", "plasma", "blood_platelets", "rbcs", "cryo"],
            "is_separable": "True" or "False"
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
            },
        },
    }

    def get(self, request):
        request_data = request.data

        if {"donation_type", "unit_type_list", "is_separable"} <= request.data.keys():
            unit_type_list = request.data["unit_type_list"] if request.data else []
            data_dict = {}

            for key in request_data["donation_type"]:
                if not unit_type_list:
                    query = self.manage_queries["donation_type"][key][
                        "model"
                    ].objects.filter(
                        # is_separable=self.manage_queries["is_separable"][request_data["is_separable"]]
                        is_separable=request_data["is_separable"]
                    )
                    if key == choices.REPLACE_DONATION:
                        query = query.exclude(operation_type=choices.EXPORT)
                    serializer = self.manage_queries["donation_type"][key]["serializer"]
                    data = serializer(query, many=True).data
                    data_dict[key] = data
                else:
                    query = self.manage_queries["donation_type"][key][
                        "model"
                    ].objects.filter(
                        unit_type__in=unit_type_list,
                        # is_separable=self.manage_queries["is_separable"][request_data["is_separable"]]
                        is_separable=request_data["is_separable"],
                    )
                    if key == choices.REPLACE_DONATION:
                        query = query.exclude(operation_type=choices.EXPORT)
                    serializer = self.manage_queries["donation_type"][key]["serializer"]
                    data = serializer(query, many=True).data
                    data_dict[key] = data

            return Response(data_dict, status=status.HTTP_200_OK)
        else:
            return Response(
                "Please Provide The Required Data !", status=status.HTTP_400_BAD_REQUEST
            )


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
                return Response(
                    "Invalid filter_in data !", status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                "Provide Required Data !", status=status.HTTP_400_BAD_REQUEST
            )
