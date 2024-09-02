from connection import Connection, convert_all_values_to_json_readable, convert_datetime_to_str
import datetime
from dateutil.relativedelta import relativedelta
import json
import sys

conn = Connection()

startdate = datetime.datetime.now()
enddate = startdate + relativedelta(months=3)
child_id = sys.argv[1]
child_details = conn.get_child_details(child_id)
grade = int(child_details["standard_id"])

wordle_words = conn.get_wordle_words(startdate, enddate, grade)

wordle_act = conn.get_wordle_act(grade)

fullActList = []

currDate = startdate + datetime.timedelta(seconds=30)

for i in wordle_words:
    wordle_activity = wordle_act
    wordle_activity["wordle_words_id"] = i["wordle_words_id"]
    wordle_activity["start_date"] = currDate
    wordle_activity["end_date"] = currDate + datetime.timedelta(hours=23, minutes=59)
    fullActList.append(wordle_activity.copy())
    currDate = currDate + datetime.timedelta(days=1)

# fullActList = convert_all_values_to_json_readable(fullActList)
# print(json.dumps(fullActList, indent=4))
conn.dump_wordle_in_child_activity(fullActList, child_id)
# print(json.dumps(fullActList.__len__(), indent=4))

