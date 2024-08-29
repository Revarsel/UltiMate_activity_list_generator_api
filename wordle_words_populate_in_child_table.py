import connection
import datetime
from dateutil.relativedelta import relativedelta
import json
import sys

conn = connection.Connection()

startdate = datetime.datetime.now() #sys.argv[3]
enddate = startdate + relativedelta(months=3)
child_id = sys.argv[1]
child_details = conn.get_child_details(child_id)
grade_num = int(child_details["standard_id"])

wordle_words = conn.get_wordle_words(startdate, enddate, grade_num)

def convert_datetime_to_str(date, data=""):
    if type(date) == str:
        print(data)
        return date
    else:
        pass
        #return date
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second
    if int(month) / 10 < 1:
        month = "0{month}".format(month=month)
    if int(day) / 10 < 1:
        day = "0{day}".format(day=day)
    if int(hour) / 10 < 1:
        hour = "0{hour}".format(hour=hour)
    if int(minute) / 10 < 1:
        minute = "0{minute}".format(minute=minute)
    if int(second) / 10 < 1:
        second = "0{second}".format(second=second)

    string = "{year}-{month}-{day} {hour}:{minutes}:{seconds}".format(year=year, month=month, day=day, hour=hour, minutes=minute, seconds=second)
    return string

wordle_act = conn.get_wordle_act(grade_num)

index = 0
for i in wordle_words:
    for k in range(len(i.keys())):
        value = list(i.values())
        keys = list(i.keys())
        if type(value[k]) == datetime.datetime:
            i[keys[k]] = convert_datetime_to_str(i[keys[k]], i)
    index += 1
index = 0

for k in range(len(wordle_act.keys())):
    value = list(wordle_act.values())
    keys = list(wordle_act.keys())
    if type(value[k]) == datetime.datetime:
        wordle_act[keys[k]] = convert_datetime_to_str(wordle_act[keys[k]], wordle_act)
index += 1

fullActList = []

currDate = startdate + datetime.timedelta(seconds=30)

for i in wordle_words:
    wordle_activity = wordle_act
    wordle_activity["wordle_words_id"] = i["wordle_words_id"]
    wordle_activity["start_date"] = currDate
    wordle_activity["end_date"] = currDate + datetime.timedelta(hours=23, minutes=59)
    fullActList.append(wordle_activity.copy())
    currDate = currDate + datetime.timedelta(days=1)

# print(json.dumps(fullActList, indent=4))
conn.dump_wordle_in_child_activity(fullActList, child_id)
# print(json.dumps(wordle_words, indent=4))

