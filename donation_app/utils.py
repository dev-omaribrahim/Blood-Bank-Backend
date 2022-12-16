# from donation_app.models import BaseDonation
import random
from . import choices

blood_convert_dict = {
   choices.A_POSITIVE: choices.A_GROUP,
   choices.A_MINUS: choices.A_GROUP,
   choices.B_POSITIVE: choices.B_GROUP,
   choices.B_MINUS: choices.B_GROUP,
   choices.O_POSITIVE: choices.O_GROUP,
   choices.O_MINUS: choices.O_GROUP,
   choices.AB_POSITIVE: choices.AB_GROUP,
   choices.AB_MINUS: choices.AB_GROUP,
   choices.A_GROUP: choices.A_GROUP,
   choices.B_GROUP: choices.B_GROUP,
   choices.O_GROUP: choices.O_GROUP,
   choices.AB_GROUP: choices.AB_GROUP,
}


def generate_serial_number(self):
    unit_types_values_dict = {
        choices.FULL_BLOOD: "FLB",
        choices.RBCs: "RBC",
        choices.PLASMA: "PLS",
        choices.BLOOD_PLATELETS: "TLT",
        choices.CRYO: "CRY"
    }

    serial_number = ""
    serial_number += unit_types_values_dict[self.unit_type]
    serial_number += self.donation_type[0].upper()
    serial_number += self.blood_type.replace("_", "").upper()
    serial_number += self.donation_create_date.strftime("%d/%m/%Y")

    if self.donation_type == choices.INSIDE_DONATION and self.is_derivative:
        serial_number += "S"

    random_num = random.randint(234567, 789000)
    try_serial_number = "{}{}".format(serial_number, random_num)
    exists_objs = self.__class__.objects.filter(unit_serial_number=try_serial_number)

    while exists_objs:
        random_num = random.randint(234567, 789000)
    else:
        serial_number = "{}{}".format(serial_number, random_num)

    return serial_number



