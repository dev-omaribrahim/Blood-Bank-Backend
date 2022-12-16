from donation_app.utils import blood_convert_dict


def convert_to_blood_group(blood_type):
    blood_group = blood_convert_dict[blood_type]
    return blood_group
