
import json

def get_filter_dict(request_data):
    black_list = ["donation_type"]
    filter_dict = {"{}__in".format(key): value for key, value in request_data.items() if key not in black_list and value != ["all"]}
    if filter_dict:
        return filter_dict
    else:
        return None
