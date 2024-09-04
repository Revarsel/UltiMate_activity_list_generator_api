from connection import Connection, convert_all_values_to_json_readable
import json
import sys
import datetime
from dateutil.relativedelta import relativedelta

if len(sys.argv) != 2:
    print("Wrong Usage. Usage is: ____.py (child_id) (activity_id)")
    exit()

conn = Connection()

child_id = sys.argv[1]
child_details = conn.get_child_details(child_id)
grade = int(child_details["standard_id"])
activity_id = sys.argv[2] # 2779

if grade >= 3:
    grade = 3
elif grade < 3:
    grade = 1

shloks = conn.get_shloks(grade)
# shloks = convert_all_values_to_json_readable(shloks)

MAC_shlok = conn.get_shlok_from_activity_id(activity_id)[0]
curr_sequence = int(MAC_shlok["sequence"])

currDate = datetime.datetime.now()
nextDate = currDate + relativedelta(weeks=2)
if (curr_sequence + 1) % 3 == 0:
    nextDate = currDate + relativedelta(months=1)

next_shlok = {}

for i in shloks:
    if int(i["sequence"]) == (curr_sequence + 1):
        next_shlok = i
        next_shlok["start_date"] = currDate
        next_shlok["end_date"] = nextDate
        break

# MAC_shlok = convert_all_values_to_json_readable(MAC_shlok)
# next_shlok = convert_all_values_to_json_readable([next_shlok])

conn.dump_data_in_child_activity([next_shlok], child_id)
# json.dump(next_shlok, sys.stdout, indent=4)
# print(next_shlok)