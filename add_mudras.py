from connection import Connection, convert_all_values_to_json_readable
import sys
import datetime
from dateutil.relativedelta import relativedelta
import json
import random

def func(val):
    if val["act_category_id"] == 2 and val["activity_game_type_id"] == 5:
        return True
    return False

def sort_activity_id(val):
    return val["activity_id"]

child_id = 40
grade = 9
weeks = 13
currDate = datetime.datetime.now()
nextDate = currDate + relativedelta(weeks=2)

conn = Connection()

mudras = conn.get_mudras(grade)
mudras = convert_all_values_to_json_readable(mudras)
existing_mudras: list = conn.get_child_activities_with_activity_table(child_id)
existing_mudras = convert_all_values_to_json_readable(existing_mudras)
existing_mudras = list(filter(func, existing_mudras))
mudras.sort(key=sort_activity_id)

fullmudralist = []

for i in range(weeks):
    if i % 2 == 1:
        continue
    rand_mudra = random.choice(mudras)
    for _ in range(1000):
        rand_mudra = random.choice(mudras)
        if rand_mudra not in existing_mudras:
            break
    rand_mudra["start_date"] = currDate
    rand_mudra["end_date"] = nextDate
    currDate = nextDate
    nextDate = currDate + relativedelta(weeks=2)
    fullmudralist.append(rand_mudra)

fullmudralist = convert_all_values_to_json_readable(fullmudralist)

json.dump(fullmudralist, sys.stdout, indent=4)

# conn.dump_data_in_child_activity(fullmudralist, child_id)