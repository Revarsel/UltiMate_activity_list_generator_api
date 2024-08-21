from connection import Connection, convert_all_values_to_json_readable
import json
import sys
import datetime
import random
from dateutil.relativedelta import relativedelta

def filter_short(data):
    if data["shlok_length_id"] == 1:
        return True
    return False

def filter_medium(data):
    if data["shlok_length_id"] == 2:
        return True
    return False

def filter_long(data):
    if data["shlok_length_id"] == 3:
        return True
    return False

def filter_shloks(data):
    if data["act_category_id"] == 2 and data["activity_game_type_id"] == 4:
        return True
    return False

def sort_activity_id(val):
    return val["activity_id"]

child_id = 40
currDate = datetime.datetime.now()
nextDate = currDate + relativedelta(weeks=2)
type_of_shlok = 1

conn = Connection()

shloks = conn.get_shloks()

shloks = convert_all_values_to_json_readable(shloks)

short = list(filter(filter_short, shloks))
medium = list(filter(filter_medium, shloks))
long = list(filter(filter_long, shloks))

existing_shloks = conn.get_existing_shloks(child_id)
existing_shloks = convert_all_values_to_json_readable(existing_shloks)
existing_id = []
previous_deities = []

sanskrit = 0
regional = 0

count = 0
for i in existing_shloks:
    existing_id.append(i["activity_id"])
    if i["deity"] not in previous_deities and i["shlok_length_id"] == type_of_shlok and count < 3:
        if i["language_id"] == 14:
            sanskrit += 1
        else:
            regional += 1
        count += 1
        previous_deities.append(i["deity"])

short_shlok = random.choice(short)
medium_shlok = random.choice(medium)
long_shlok = random.choice(long)

match type_of_shlok:
    case 1:
        for i in range(1000):
            if short_shlok["deity"] not in previous_deities and short_shlok["activity_id"] not in existing_id:
                if regional >= 1 and short_shlok["language_id"] == 14:
                    continue
                short_shlok["start_date"] = currDate
                short_shlok["end_date"] = nextDate
                conn.dump_data_in_child_activity([short_shlok], child_id)
                break
            short_shlok = random.choice(short)

    case 2:
        for i in range(1000):
            if medium_shlok["deity"] not in previous_deities and medium_shlok["activity_id"] not in existing_id:
                medium_shlok["start_date"] = currDate
                medium_shlok["end_date"] = nextDate
                conn.dump_data_in_child_activity([medium_shlok], child_id)
                break
            medium_shlok = random.choice(medium)

    case 3:
        for i in range(1000):
            if long_shlok["deity"] not in previous_deities and long_shlok["activity_id"] not in existing_id:
                long_shlok["start_date"] = currDate
                long_shlok["end_date"] = nextDate
                conn.dump_data_in_child_activity([long_shlok], child_id)
                break
            long_shlok = random.choice(long)

json.dump(previous_deities, sys.stdout, indent=4)