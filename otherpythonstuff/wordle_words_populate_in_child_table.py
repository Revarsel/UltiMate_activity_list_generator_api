from connection import Connection, convert_all_values_to_json_readable
import datetime
from dateutil.relativedelta import relativedelta
import json
import sys

conn = Connection()

child_id = sys.argv[1]
child_details = conn.get_child_details(child_id)
user_id = int(child_details["user_id"])
grade_num = int(child_details["standard_id"])

subscription = conn.get_subscription_from_child_id(child_id) # returns all subscriptions of the user in descending order
if len(subscription) == 0:
    raise Exception("No subscription found!")

start_date: datetime.datetime = subscription[0]["start_date"]
end_date: datetime.datetime = subscription[0]["end_date"]

wordle_words = conn.get_wordle_words(start_date, end_date, grade_num)

wordle_act = conn.get_wordle_act(grade_num)

fullActList = []

currDate = start_date + datetime.timedelta(seconds=30)

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